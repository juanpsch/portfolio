# consultora/urls.py

from django.urls import path
from . import views
from .api_views import chatbot_api

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
    path('contact/', views.contact_form_submit, name='contact_submit'),
]