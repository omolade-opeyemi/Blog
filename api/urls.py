from django.urls import path
from . views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [

    path('', PostList.as_view()),
    path('comment',CommentList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('register/',UserCreateView.as_view()),
    path('login/',UserLoginSerializer.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]