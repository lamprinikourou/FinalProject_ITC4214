from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        # Process the form (just capture the data here for simplicity)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # You can add form validation or send an email here if needed
        
        # Add a success message to display
        messages.success(request, "Your message was sent successfully!")

    # Render the contact page
    return render(request, 'core/contact.html')

def shop(request):
    return render(request, 'core/shop.html')


from django.shortcuts import redirect

def login_redirect(request):
    return redirect('accounts:login')

def register_redirect(request):
    return redirect('accounts:register')

def profile_redirect(request):
    return redirect('accounts:profile')

# core/views.py
from django.shortcuts import render
from django.urls import reverse

def shop(request):
    return render(request, 'core/shop.html', {'catalog_url': reverse('catalog:catalog_home')})
