from django.urls import path
from . import views

urlpatterns = [
    path('register.html', views.registerPage, name='registerU'),
    path('login.html', views.loginPage, name='loginU'),
    path('logout.html', views.logoutPage, name='logoutU'),
]

