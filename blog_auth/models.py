from django.db import models
from django.contrib.auth.models import User

def user_profile_image_path(instance, filename):
    return f'profile_pictures/{instance.user.username}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_profile_image_path, default='profile_pictures/default.jpg')

    def __str__(self):
        return str(self.user)

