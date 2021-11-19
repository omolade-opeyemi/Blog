
from django.urls import path
from . import views

urlpatterns = [
    path('post.html', views.addPostPage, name='add_post'),
    path('update/<str:pk>/', views.updatePage, name='update'),
    path('delete/<str:pk>/', views.deletePage, name='delete'),
    
]

