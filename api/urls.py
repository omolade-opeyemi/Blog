from django.urls import path
from knox import views as knox_views
from . views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    path('', PostList.as_view()),
    path('comment',CommentList.as_view()),
    path('users',UserDetailList.as_view()),
    path('likes',LikeList.as_view()),
    path('likes/<int:pk>/', LikeDetail.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    #path('register/',UserCreateView.as_view()),
    path('register/', RegisterAPI.as_view(), name='register'),
    #path('login/',UserLoginSerializer.as_view()),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]