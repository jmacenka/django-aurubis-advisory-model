# material_handler/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class MaterialHandlerLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/material_handler/') and not request.user.is_authenticated:
            return redirect('{}?next={}'.format(reverse('login'), request.path))
        response = self.get_response(request)
        return response
