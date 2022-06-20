from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login,authenticate,logout
from .forms import NewUserForm,ProfileForm,ExistingUserChangeForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.decorators import login_required
from .models import Profile,User
from django.contrib.auth import get_user_model



# Create your views here.
User = get_user_model()

def index(request):
    return render(request, 'index.html',)

def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Registration Successful.')
        return redirect('homepage')
    messages.error(request, 'Unsuccessful registration. Invalid information.')
    form = NewUserForm()
    return render(request, 'registration/registration_form.html', {"registration_form": form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {username}.")
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid Username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'registration/login_form.html', {"login_form": form})


def logout_user(request):
    
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')