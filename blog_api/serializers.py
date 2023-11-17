from blog_post.models import Category, Post
from blog_comment.models import Comment
from rest_framework import serializers
from django.contrib.auth.models import User
from blog_auth.models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.urls import reverse
from django.shortcuts import get_object_or_404

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    post_title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('url', 'post_title', 'author_name', 'content', 'created_date', 'updated_date')
        read_only_fields = ('post', 'created_date', 'updated_date', 'author')

    def get_url(self, obj):
        post_slug = obj.post.slug 
        return reverse('post-comment-detail', kwargs={'post_slug': post_slug, 'pk': obj.pk})


    def get_author_name(self, obj):
        return obj.author.username

    def get_post_title(self, obj):
        return obj.post.title
    
    def create(self, validated_data):
        post_slug = self.context['view'].kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = post
        return super(CommentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if instance.author == self.context['request'].user:
            instance.content = validated_data.get('content', instance.content)
            instance.updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            instance.save()
            return super(CommentSerializer, self).update(instance, validated_data)
        else:
            raise serializers.ValidationError("You do not have permission to edit this comment.")

class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments_url = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='slug', lookup_url_kwarg='slug')
    class Meta:
        model = Post
        fields = ('url', 'title', 'content', 'category', 'author_name', 'created_date', 'updated_date', 'comments_url')
        read_only_fields = ('created_date', 'updated_date', 'author', 'slug')

    def get_author_name(self, obj):
        return obj.author.username

    def get_comments_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('post-comments', args=[obj.slug]))
        return None

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super(PostSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if instance.author == self.context['request'].user:
            instance.title = validated_data.get('title', instance.title)
            instance.content = validated_data.get('content', instance.content)
            instance.category = validated_data.get('category', instance.category)
            instance.updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            instance.save()
            return super(PostSerializer, self).update(instance, validated_data)
        else:
            raise serializers.ValidationError("You do not have permission to edit this post.")
   
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('No user found with this email.')
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uidb64, token

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirmation = data.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise serializers.ValidationError("New password and confirmation do not match.")

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        new_password = data.get('new_password')
        new_password_confirmation = data.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise serializers.ValidationError("New password and confirmation do not match.")

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        new_username = user_data.get('username', instance.user.username)
        if new_username != instance.user.username and UserProfile.objects.filter(user__username=new_username).exists():
            raise serializers.ValidationError("Username already exists.")

        new_email = user_data.get('email', instance.user.email)
        if new_email != instance.user.email and UserProfile.objects.filter(user__email=new_email).exists():
            raise serializers.ValidationError("Email already exists.")
        instance.user.username = new_username
        instance.user.email = new_email
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.save()
        instance.save()
        return super(UserProfileSerializer, self).update(instance, validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("This username is already in use.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("This email address is already in use.")
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        UserProfile.objects.create(user=user)
        return user

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name']

