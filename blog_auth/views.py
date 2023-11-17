from django.shortcuts import render, HttpResponse, redirect
from blog_auth.forms import UserSignupForm, UserProfileForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog_auth.models import UserProfile 

# Create your views here.

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST) 
        if form.is_valid():
            user=form.save()
            UserProfile(user=user).save()
            messages.success(request, "User Account Created Successfully.")
            return redirect("login")
    else:
        form = UserSignupForm()
    return render(request, 'blog_auth/signup.html', {'form': form})

@login_required
def user_profile(request):
    # user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile') 
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        # profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'blog_auth/profile.html', {'user_form': user_form})
    # return render(request, 'blog_auth/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'user_profile':user_profile})