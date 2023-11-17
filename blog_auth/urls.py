from django.urls import path
from blog_auth.views import user_signup, user_profile
from blog_auth.forms import CustomAuthenticationForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    #Signup and Login
    path('signup/', user_signup, name="user_signup"),
    path('login/', LoginView.as_view(template_name="blog_auth/login.html", authentication_form=CustomAuthenticationForm,), name="login"),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),

    #Change Password
    path('password_change/', PasswordChangeView.as_view(template_name="blog_auth/password_change.html", form_class=MyPasswordChangeForm), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="blog_auth/password_change_done.html"), name="password_change_done"),

    #Reset Password
    path('password_reset/', PasswordResetView.as_view(template_name="blog_auth/password_reset.html", form_class=MyPasswordResetForm), name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="blog_auth/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="blog_auth/password_reset_confirm.html", form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="blog_auth/password_reset_complete.html"), name="password_reset_complete"),
    
    #profile
    path('profile/', user_profile, name="user_profile"),


]