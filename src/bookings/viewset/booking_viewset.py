import base64
import os

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from msal import ConfidentialClientApplication
import requests
import logging
from msal import ConfidentialClientApplication
from rest_framework.decorators import action
from bookings.serializer.booking_serializer import BookingRoomSerializer
from bookings.models.booking_room_models import BookingRoomsModels
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

logger = logging.getLogger(__name__)

class BookingRoomViewSet(viewsets.ModelViewSet):
    queryset = BookingRoomsModels.objects.all()
    serializer_class = BookingRoomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )




    @staticmethod
    def obtenir_access_token():
        CLIENT_ID = "d93aec86-9778-43c2-aac3-caec89341ad7"
        TENANT_ID =  "consumers"#"common"#"e6467647-4f44-4d7b-9bc7-4893c31f2c76"  # ou "common" si compte personnel
        CLIENT_SECRET = "hvd8Q~pQNvHdf2OzksM9D0HCDtZ.ygARdMJQnc6j"
        AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
        SCOPES = ["https://graph.microsoft.com/.default"]

        try:
            app = ConfidentialClientApplication(
                client_id=CLIENT_ID,
                client_credential=CLIENT_SECRET,
                authority=AUTHORITY
            )

            result = app.acquire_token_for_client(scopes=SCOPES)

            if "access_token" in result:
                return result["access_token"]
            else:
                logger.error(f"Échec lors de la récupération du token : {result}")
                raise Exception("Impossible d'obtenir le token d'accès.")
        except Exception as e:
            logger.error(f"Erreur lors de l'obtention du token : {str(e)}")
            raise


    @staticmethod
    def type_email(email):

        if email.endswith('@outlook.com') or email.endswith('@hotmail.com') or email.endswith('@live.com'):
            return 'microsoft'
        return 'other'

    def envoyer_email_microsoft(self, access_token, sujet, message, destinataire, sender_email):
        url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        email = {
            "message": {
                "subject": sujet,
                "body": {
                    "contentType": "Text",
                    "content": message
                },
                "toRecipients": [
                    {"emailAddress": {"address": destinataire}}
                ]
            }
        }
        try:
            response = requests.post(url, json=email, headers=headers)
            response.raise_for_status()
            logger.info("Email envoyé avec succès via Microsoft Graph.")
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Erreur HTTP lors de l'envoi de l'email via Microsoft Graph : {e.response.status_code} {e.response.text}")
            raise Exception(f"Échec de l'envoi de l'email : {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de l'envoi de l'email via Microsoft Graph : {str(e)}")
            raise Exception("Une erreur réseau s'est produite lors de l'envoi de l'email.")


    def creer_evenement_outlook_calendar(self, reservation, access_token):
        sender_email = "hienronsard@gmail.com"
        url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/events"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        evenement = {
            "subject": f"Réunion : {reservation.salle.name}",
            "body": {
                "contentType": "HTML",
                "content": f"Réservée par {reservation.user.username}."
            },
            "start": {
                "dateTime": f"{reservation.date}T{reservation.heure_debut}",
                "timeZone": "Africa/Abidjan"
            },
            "end": {
                "dateTime": f"{reservation.date}T{reservation.heure_fin}",
                "timeZone": "Africa/Abidjan"
            },
            "location": {
                "displayName": reservation.salle.localisation
            }
        }
        try:
            response = requests.post(url, json=evenement, headers=headers)
            response.raise_for_status()
            logger.info("Événement ajouté avec succès à Outlook Calendar.")
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Erreur HTTP lors de l'ajout de l'événement à Outlook : {e.response.status_code} {e.response.text}")
            raise Exception(f"Impossible de créer l'événement dans Outlook : {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur réseau lors de la création de l'événement : {str(e)}")
            raise Exception("Une erreur réseau s'est produite lors de la création de l'événement.")

    def envoyer_email_confirmation(self, reservation):
        sujet = f"Confirmation de réservation - {reservation.salle.name}"
        message = (
            f"Bonjour {reservation.user.username},\n\n"
            f"Votre réservation pour la salle {reservation.salle.name} a été validée.\n"
            f"Date : {reservation.date}\n"
            f"Horaire : {reservation.heure_debut} - {reservation.heure_fin}\n"
            f"Statut : {reservation.etat}\n\n"
            f"Cordialement,\nL'équipe de gestion des salles."
        )

        email_type = self.type_email(reservation.user.email)
        sender_email = "hienronsard@gmail.com"

        if email_type == 'microsoft':
            try:
                access_token = self.obtenir_access_token()
                self.envoyer_email_microsoft(access_token, sujet, message, reservation.user.email, sender_email)
            except Exception as e:
                logger.error(f"Échec de l'envoi via Microsoft Graph : {str(e)}")

                try:
                    self.envoyer_email_google(sujet, message, reservation.user.email)
                except Exception as e_google:
                    logger.error(f"Échec de l'envoi via Google Gmail : {str(e_google)}")
        else:
            try:
                send_mail(sujet, message, 'admin@portabidjan.ci', [reservation.user.email])
            except Exception as e:
                logger.error(f"Échec de l'envoi via Django SMTP : {str(e)}")


    @action(detail=False, methods=['post'])
    def send_reservation(self, request, pk=None):
        serializer = BookingRoomSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            salle = data['salle']
            utilisateur = data['user']

            if not salle or not utilisateur:
                return Response({"error": "Salle ou utilisateur invalide."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if utilisateur.direction == salle.direction:
                    reservation = serializer.save(etat='validee')


                    try:
                        self.envoyer_email_confirmation(reservation)
                    except Exception as e:
                        logger.error(f"Erreur lors de l'envoi de l'email : {str(e)}")


                    try:
                        self.creer_evenement_google_calendar(reservation)
                    except Exception as e:
                        logger.error(f"Erreur lors de la création de l'événement Google Calendar : {str(e)}")

                    return Response(
                        {"message": "Réservation validée automatiquement (avec ou sans notifications).",
                         "data": serializer.data},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    reservation = serializer.save(etat='en_attente')
                    try:
                        self.notifier_secretaire(reservation)
                    except Exception as e:
                        logger.error(f"Erreur lors de la notification au secrétaire : {str(e)}")

                    return Response(
                        {"message": "Réservation en attente de validation (avec ou sans notifications).",
                         "data": serializer.data},
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                logger.error(f"Erreur lors de l'enregistrement de la réservation : {str(e)}")
                return Response({"error": f"Erreur interne : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def notifier_secretaire(reservation):
        secretaire_email = reservation.salle.direction.secretaire.email
        sujet = f"Nouvelle réservation en attente - {reservation.salle.name}"
        message = (
            f"Bonjour,\n\n"
            f"Une nouvelle réservation est en attente de validation pour la salle {reservation.salle.name}.\n"
            f"Date : {reservation.date}\n"
            f"Horaire : {reservation.heure_debut} - {reservation.heure_fin}\n"
            f"Réservée par : {reservation.user.username}\n\n"
            f"Veuillez valider ou rejeter cette réservation via le système.\n\n"
            f"Cordialement,\nL'équipe de gestion des salles."
        )
        send_mail(sujet, message, 'admin@portabidjan.ci', [secretaire_email])

    def envoyer_email_google(self, sujet, message, destinataire):
        try:

            SCOPES = ['https://www.googleapis.com/auth/gmail.send']
            SERVICE_ACCOUNT_FILE = 'config/credentials/credentials.json'

            credentials = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )


            service = build('gmail', 'v1', credentials=credentials)


            email_message = f"""\
                                    From: "Port Abidjan" <admin@portabidjan.ci>
                                    To: {destinataire}
                                    Subject: {sujet}

                                    {message}
            """
            raw_email = {'raw': base64.urlsafe_b64encode(email_message.encode("utf-8")).decode("utf-8")}

            # Envoi de l'email
            service.users().messages().send(userId='me', body=raw_email).execute()
            logger.info("Email envoyé avec succès via Google Gmail.")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email via Google Gmail : {str(e)}")
            raise Exception("Une erreur s'est produite lors de l'envoi de l'email via Gmail.")



    def creer_evenement_google_calendar(self, reservation):

        try:
            # Déterminer le chemin absolu vers les credentials
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'config', 'credentials', 'credentials.json')
            SCOPES = ['https://www.googleapis.com/auth/calendar']

            # Log pour vérifier le chemin
            logger.info(f"Chemin du fichier credentials.json : {SERVICE_ACCOUNT_FILE}")

            # Charger les credentials
            credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('calendar', 'v3', credentials=credentials)

            # Construire les données de l'événement
            event = self.construire_donnees_evenement(reservation)

            # Log pour afficher l'événement avant l'envoi
            logger.info(f"Données de l'événement envoyé à Google Calendar : {event}")

            # Ajouter l'événement dans le calendrier principal
            calendar_id = 'primary'
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

            # Log pour confirmer la création
            logger.info(f"Événement créé avec succès dans Google Calendar : {created_event.get('htmlLink')}")
            return created_event.get('htmlLink')
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'événement dans Google Calendar : {str(e)}")
            raise Exception("Une erreur s'est produite lors de la création de l'événement Google Calendar.")

    def construire_donnees_evenement(self, reservation):

        # Validation des champs critiques
        if not reservation.date or not reservation.heure_debut or not reservation.heure_fin:
            raise ValueError("Les champs date, heure_debut et heure_fin sont obligatoires.")

        if reservation.heure_debut >= reservation.heure_fin:
            raise ValueError("L'heure de fin doit être postérieure à l'heure de début.")

        if not reservation.user.email:
            raise ValueError("L'utilisateur doit avoir une adresse email valide.")


        return {
            'summary': f"Réunion : {reservation.salle.name}",
            'location': reservation.salle.localisation or 'Emplacement non spécifié',
            'description': f"Réservation effectuée par {reservation.user.username}.",
            'start': {
                'dateTime': f"{reservation.date}T{reservation.heure_debut.strftime('%H:%M:%S')}",
                'timeZone': 'Africa/Abidjan',
            },
            'end': {
                'dateTime': f"{reservation.date}T{reservation.heure_fin.strftime('%H:%M:%S')}",
                'timeZone': 'Africa/Abidjan',
            },
            'attendees': [
                {'email': reservation.user.email},
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

    def envoyer_email_statut_reservation(self, reservation, statut):
        sujet = f"Mise à jour de votre réservation pour - {reservation.salle.name}"
        if statut == 'validee':
            message = (
                f"Bonjour {reservation.user.username},\n\n"
                f"Votre réservation pour la salle {reservation.salle.name} a été validée.\n"
                f"Date : {reservation.date}\n"
                f"Horaire : {reservation.heure_debut} - {reservation.heure_fin}\n"
                f"Statut : {statut}\n\n"
                f"Cordialement,\nL'équipe de gestion des salles."
            )
        elif statut == 'rejete':
            message = (
                f"Bonjour {reservation.user.username},\n\n"
                f"Votre réservation pour la salle {reservation.salle.name} a été refusée.\n"
                f"Date : {reservation.date}\n"
                f"Horaire : {reservation.heure_debut} - {reservation.heure_fin}\n"
                f"Statut : {statut}\n\n"
                f"Cordialement,\nL'équipe de gestion des salles."
            )


        email_type = self.type_email(reservation.user.email)
        sender_email = "admin@portabidjan.ci"

        if email_type == 'microsoft':
            try:
                access_token = self.obtenir_access_token()
                self.envoyer_email_microsoft(access_token, sujet, message, reservation.user.email, sender_email)
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de l'email via Microsoft Graph : {str(e)}")
        else:
            try:
                send_mail(sujet, message, sender_email, [reservation.user.email])
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de l'email via SMTP : {str(e)}")




    @action(detail=False, methods=['get'], url_path='pending-reservations')
    def get_pending_reservations(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "Utilisateur non authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.role == 'super_admin':
            pending_reservations = BookingRoomsModels.objects.filter(etat='en_attente')
        else:

            if not user.direction:
                return Response(
                    {"error": "L'utilisateur n'est pas associé à une direction."},
                    status=status.HTTP_403_FORBIDDEN
                )


            pending_reservations = BookingRoomsModels.objects.filter(
                salle__direction=user.direction,
                etat='en_attente'
            )

        serializer = self.get_serializer(pending_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):

        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "Utilisateur non authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            reservation = BookingRoomsModels.objects.get(pk=pk)
        except BookingRoomsModels.DoesNotExist:
            return Response({"error": "Réservation non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'super_admin':
            if not hasattr(user, 'direction') or reservation.salle.direction != user.direction:
                return Response(
                    {"error": "Vous n'êtes pas autorisé à modifier cette réservation."},
                    status=status.HTTP_403_FORBIDDEN
                )

        new_status = request.data.get('etat')
        if new_status not in ['validee', 'rejete']:
            return Response(
                {"error": "Statut invalide. Seuls 'validee' et 'rejete' sont autorisés."},
                status=status.HTTP_400_BAD_REQUEST
            )

        reservation.etat = new_status
        reservation.save()

        try:
            self.envoyer_email_statut_reservation(reservation, new_status)
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de notification : {str(e)}")

        return Response(
            {"message": f"Réservation mise à jour avec succès à '{new_status}'."},
            status=status.HTTP_200_OK
        )


    @action(detail=True, methods=['post'], url_path='cancel-reservation')
    def cancel_reservation(self, request, pk=None):
        user = request.user


        if not user.is_authenticated:
            return Response(
                {"error": "Utilisateur non authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )


        try:
            reservation = BookingRoomsModels.objects.get(pk=pk)
        except BookingRoomsModels.DoesNotExist:
            return Response({"error": "Réservation non trouvée."}, status=status.HTTP_404_NOT_FOUND)


        if reservation.user != user:
            return Response(
                {"error": "Vous n'êtes pas autorisé à annuler cette réservation."},
                status=status.HTTP_403_FORBIDDEN
            )


        if reservation.etat not in ['en_attente']:
            return Response(
                {"error": f"La réservation ne peut pas être annulée car elle est dans l'état '{reservation.etat}'."},
                status=status.HTTP_400_BAD_REQUEST
            )


        reservation.etat = 'annulee'
        reservation.save()


        try:
            self.envoyer_email_statut_reservation(reservation, 'annulee')
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de notification : {str(e)}")

        return Response(
            {"message": "Réservation annulée avec succès."},
            status=status.HTTP_200_OK
        )


    @action(detail=True, methods=['post'], url_path='release')
    def release_room(self, request, pk=None):
        user = request.user

        if not user.is_authenticated:
            return Response(
                {"error": "Utilisateur non authentifié."},
                status=status.HTTP_401_UNAUTHORIZED
            )


        try:
            reservation = BookingRoomsModels.objects.get(pk=pk)
        except BookingRoomsModels.DoesNotExist:
            return Response({"error": "Réservation non trouvée."}, status=status.HTTP_404_NOT_FOUND)


        if reservation.user != user:
            return Response(
                {"error": "Vous n'êtes pas autorisé à libérer cette salle."},
                status=status.HTTP_403_FORBIDDEN
            )


        if reservation.etat != 'validee':
            return Response(
                {
                    "error": f"La salle ne peut pas être libérée car la réservation est dans l'état '{reservation.etat}'."},
                status=status.HTTP_400_BAD_REQUEST
            )


        reservation.etat = 'libere'
        reservation.save()


        logger.info(
            f"La réservation {reservation.id} pour la salle {reservation.salle.name} a été libérée par {user.username}.")

        return Response(
            {"message": "La salle a été libérée avec succès."},
            status=status.HTTP_200_OK
        )

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return BookingRoomsModels.objects.none()

        if user.role == 'employe':
            return BookingRoomsModels.objects.filter(user=user)

        return BookingRoomsModels.objects.all()