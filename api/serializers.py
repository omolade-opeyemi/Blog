from rest_framework import serializers
from Blog.models import Post, Comment
from django.contrib.auth.models import User
from django.db.models import Q


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'likes', )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'active', )

class UserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')
        email = validated_data.pop('email', '')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('password mismatch')
        
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError('Email Taken')

    
        user = User.objects.create(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    class Meta:
        model = User
        fields = (
            'id',
            'token',
            'username',
            'password',           
        )
        extra_kwargs = {
            'password':{'write_only':True}
        }
    # def validate(self, data):
    #     user_obj = None
    #     username = data.get('username')
    #     password = data['password']
    #     user = User.objects.filter(Q(username=username)).distinct()
    #     if not username:
    #         raise ValidationError('Username is required')
    #     if user.exists() and user.count() == 1:
    #         user_obj = user.first()
    #     else:
    #         raise serializers.ValidationError('invalid username')
    #     if user_obj:
    #         if not user_obj.check_password(password):
    #             raise serializers.ValidationError('incorrect credentials')
    #     data['token'] = 'some random token'
    #     return data



   

