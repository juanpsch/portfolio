# consultora/views.py

from django.shortcuts import render

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

def home(request):
    """
    Esta vista renderiza la página principal de la consultora.
    """
    return render(request, 'consultora/index.html')


# your_app/views.py
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

def contact_form_submit(request):
    if request.method == 'POST':
        name = request.POST.get('nombre')
        email = request.POST.get('email')
        message = request.POST.get('mensaje')

        subject = f'New contact message from: {name}'
        message_body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['jpautomake@gmail.com']

        send_mail(subject, message_body, from_email, recipient_list)

        return redirect('home')

    return render(request, 'consultora/index.html')