from django.http import JsonResponse

def consent_callback(request):
    error = request.GET.get("error")
    if error:
        return JsonResponse({"status": "failed", "message": f"Consentement échoué : {error}"})
    return JsonResponse({"status": "success", "message": "Consentement accordé avec succès."})
