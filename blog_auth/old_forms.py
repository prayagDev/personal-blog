from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from blog_auth.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class CustomUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise forms.ValidationError('This email is already in use. Please use a different email address.')
        return email

class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput(attrs={'class':'form-control'}))

    error_messages={
        'password_mismatch':'New Password Confirmation is not matched with New Password..'
    }

class MyPasswordResetForm(PasswordResetForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("This email address is not registered.")
        return email

class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2=forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    error_messages={
        'password_incorrect':'Your entered password is not correct',
        'password_mismatch':'Confirm New Password is not matched with New Password ..',
    }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
class UserSignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    class Meta:
        model=User
        fields=['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    error_messages = {
        'password_mismatch': "Confirm Password did not match with Password..",
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email