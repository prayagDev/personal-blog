from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm
from blog_auth.models import UserProfile

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class CustomUserChangeForm(BaseForm, UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            raise forms.ValidationError('This email is already in use. Please use a different email address.')
        return email

class MySetPasswordForm(BaseForm, SetPasswordForm):
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput())
    new_password2=forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput())

    error_messages={
        'password_mismatch':'New Password Confirmation is not matched with New Password..'
    }

class MyPasswordResetForm(BaseForm, PasswordResetForm):
    # email=forms.CharField(widget=forms.EmailInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("This email address is not registered.")
        return email

class MyPasswordChangeForm(BaseForm, PasswordChangeForm):
    # old_password=forms.CharField(widget=forms.PasswordInput())
    new_password1=forms.CharField(label="New Password", widget=forms.PasswordInput())
    new_password2=forms.CharField(label="Confirm new password", widget=forms.PasswordInput())
    error_messages={
        'password_incorrect':'Your entered password is not correct',
        'password_mismatch':'Confirm New Password is not matched with New Password ..',
    }


class CustomAuthenticationForm(BaseForm, AuthenticationForm):
    # username = forms.CharField(widget=forms.TextInput(), max_length=30)
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pass
    
class UserSignupForm(BaseForm, UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(),
    )
    class Meta:
        model=User
        fields=['username', 'email']

        widgets = {
            'username': forms.TextInput(),
        }
        
    error_messages = {
        'password_mismatch': "Confirm Password did not match with Password..",
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email