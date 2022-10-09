from django.http import JsonResponse


def index(request):
    response = {"status": "ok"}
    return JsonResponse(response, status=200)
