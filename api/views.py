from Blog.models import Post, Comment
from .serializers import *
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .permissions import ReadOnly
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings
from django.contrib import auth
import jwt
from rest_framework import viewsets

from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView

# Create your views here.
class PostList(generics.ListCreateAPIView):
    #parser_classes = (FormParser,MultiPartParser)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["Heading","SubHeading","Content", 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authencation_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,active=True)
class LikeList(generics.ListCreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, request, format=None):
        serializer=LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    authencation_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserDetailList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserDetailSerializer

class UserCreateView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UsercreateSerializer

# class UserLoginSerializer(GenericAPIView):
#     permission_classes=[AllowAny]
#     serializer_class = UserLoginSerializer

#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             new_data = serializer.data
#             return Response(new_data, status=200)
#         return Response(serializer.errors, status=400)


# class UserLoginSerializer(GenericAPIView):
#     permission_classes=[AllowAny]
#     serializer_class = UserLoginSerializer
#     def post(self, request):
#         data=request.data
#         username = data.get('username', '')
#         password = data.get('password','')
#         user = auth.authenticate(username=username, password=password)
#         if user:
#             auth_token=jwt.encode({'username':user.username}, settings.JWT_SECRET_KEY)
#             serializer=UserLoginSerializer(user)
#             data={
#                 'user':serializer.data,
#                 'token': auth_token
#             }
#             return response(data, status=200)
#         return response({'detail':invalid}, status=401)

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
       
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
        

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer


    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
       
    