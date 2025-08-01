from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    """
    Handles user registration. If the request is a POST, it processes the
    registration form. Otherwise, it displays a blank registration form.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # Saves the new user to the database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
