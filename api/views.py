from Blog.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer,UserLoginSerializer
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

from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView




# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["Heading","SubHeading","Content", 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,likes=self.likes.count())

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authencation_classes = (TokenAuthentication,)
    permission_classes = permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly]


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,active=True)

class UserCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginSerializer(GenericAPIView):
    permission_classes=[AllowAny]
    serializer_class = UserLoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_data = serializer.data
            return Response(new_data, status=200)
        return Response(serializer.errors, status=400)


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

    