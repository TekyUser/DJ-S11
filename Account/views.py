from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User

def delete_account(request):
    user = request.user
    user.delete()  # Delete the user account
    logout(request)  # Log the user out
    messages.success(request, 'Your account has been deleted.')
    return redirect('home')  # Redirect to home page after deletion

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home view
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home view
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def account_detail_and_change_password(request):
    # Get the currently logged-in user
    user = request.user
    # Handle password change form
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Important to keep the user logged in after password change
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('account_detail')  # Redirect to the account detail page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(user=user)
    # Pass the form to the template
    return render(request, 'account/account_detail.html', {'user': user, 'form': form})