from django.urls import path
from. import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('contact.html', views.contactPage, name='contact'),
    path('post.html/<str:pk>/', views.postPage, name='post'),
    path('profile.html/<str:pk>/', views.userPage, name='profile'),
    path('like/<str:pk>/', views.likePage, name='like'),
    path('edit.html', views.editProfile, name='edit'),
]

