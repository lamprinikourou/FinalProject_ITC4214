# core/urls.py
from django.urls import path
from . import views

app_name = 'core'  

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('shop/', views.shop, name='shop'),  # Shop page
]
