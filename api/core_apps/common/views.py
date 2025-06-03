from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def health_check(request):
    """
    Health check endpoint to verify the API is running.
    """
    return JsonResponse({
        "status": "ok",
        "message": "API is running",
    })
