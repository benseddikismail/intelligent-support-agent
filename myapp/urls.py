from django.urls import path
from myapp import views

urlpatterns = [
	path('', views.home, name = 'home'),
	path('webhook/', views.webhook, name='webhook'),
	path('contact/', views.contact, name='contact'),
	path('popup/', views.popup, name='popup'),
]