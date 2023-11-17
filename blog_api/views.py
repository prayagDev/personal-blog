from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet
from blog_post.models import Category
from blog_auth.models import UserProfile
# from blog_api.serializers import CategorySerializer, CategoryListSerializer, UserSignupSerializer, UserLoginSerializer, UserProfileSerializer, ChangePasswordSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, PostSerializer, CommentSerializer
from blog_api.serializers import *
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from blog_api.email_utils import send_email
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_date")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user == instance.author:
            self.perform_destroy(instance)
            return Response({"detail": "post deleted."}, status=204)
        else:
            return Response({"detail": "You do not have permission to delete this post."}, status=403)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        return Comment.objects.filter(post__slug=post_slug)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user == instance.author:
            self.perform_destroy(instance)
            return Response({"detail": "comment deleted."}, status=204)
        else:
            return Response({"detail": "You do not have permission to delete this comment."}, status=403)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            to_email=serializer.validated_data['email']
            uidb64, token = serializer.save()
            # Construct the reset link
            current_site = get_current_site(request)
            # Using reverse to generate the URL based on the pattern name
            reset_link = f'http://{current_site.domain}{reverse("password-reset-confirm", args=[uidb64, token])}'
            message="Click on this link to reset your password \n "+ reset_link
            subject="reset your password"
            send_email(to_email, subject, message)

            return Response({'message': 'Password reset email sent successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))
            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

            if default_token_generator.check_token(user, token):
                # Set the new password
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                
                return Response({'message': 'Password reset successfully'})
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # Check old password
            if not user.check_password(old_password):
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

            # Change password
            user.set_password(new_password)
            user.save()

            # Update session authentication hash
            update_session_auth_hash(request, user)

            return Response({'message': 'Password changed successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully.'})
        return Response(serializer.errors, status=400)

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return CategoryListSerializer
    #     return CategorySerializer

