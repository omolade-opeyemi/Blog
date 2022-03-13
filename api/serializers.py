from rest_framework import serializers
from Blog.models import Post, Comment, Likes
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.fields import SerializerMethodField

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
            'id','username','email','first_name','last_name'
        ]


class PostSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True)
    total_likes = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = '__all__'
    def get_total_likes(self, instance):
        return instance.likes.count()

class LikesSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = Likes
        fields = '__all__'
        read_only_fields = ('active', )
    def get_total_likes(self, instance):
        return instance.like.count()
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'active', )

class UsercreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=128, write_only=True, label='password')
    password2 = serializers.CharField(max_length=128, write_only=True, label='confirm password')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'password1',
            'password2',
        )
        read_only_fields = ('id', 'is_staff', 'is_superuser','password',)

    def validate(self, data):
        password1 = data['password1']
        password2 = data['password2']
        email = data['email']
        if password1 != password2:
            raise serializers.ValidationError('password mismatch')

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email Taken')
        return super().validate(data)

    def create(self, validated_data): 
        password1 = validated_data.pop('password1')
        user = User.objects.create_user(**validated_data)
        user.set_password(password1)
        user.save()
        return user

# class UserLoginSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(read_only=True)
#     username = serializers.CharField()
#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'token',
#             'username',
#             'password',           
#         )
#         extra_kwargs = {
#             'password':{'write_only':True}
#         }
#     def validate(self, data):
#         user_obj = None
#         username = data.get('username')
#         password = data.get('password')
#         user = User.objects.filter(Q(username=username)).distinct()
#         if not username:
#             raise ValidationError('Username is required')
#         if user.exists() and user.count() == 1:
#             user_obj = user.first()
#         else:
#             raise serializers.ValidationError('invalid username')
#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise serializers.ValidationError('incorrect credentials')
#         # data['token'] = 'some random token'
#         return data

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password','id')
        extra_kwargs = {'password': {'write_only': True}}



   

