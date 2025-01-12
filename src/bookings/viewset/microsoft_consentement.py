from django.shortcuts import redirect

def obtenir_consentement(request):
    CLIENT_ID = "d93aec86-9778-43c2-aac3-caec89341ad7"
    REDIRECT_URI = "http://localhost:8000/api/V1/bookings/consent_callback/"
    AUTHORITY = "https://login.microsoftonline.com/common/adminconsent"

    consent_url = f"{AUTHORITY}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(consent_url)
