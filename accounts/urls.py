from django.urls import path
from . import views

urlpatterns = [
    path('register.html', views.registerPage, name='register'),
    path('login.html', views.loginPage, name='login'),
    path('logout.html', views.logoutPage, name='logout'),
]

