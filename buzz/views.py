from django.shortcuts import get_object_or_404, render,redirect
from django.http import Http404, HttpResponseRedirect, JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from itertools import chain
from .models import Neighborhood, User, Profile, Business, Post
from .forms import NewUserForm,ProfileForm,ExistingUserChangeForm,NeighborhoodForm,BusinessForm
from .email import send_welcome_email




# Create your views here.
User = get_user_model()

def index(request):
    return render(request, 'index.html',)

def register_user(request):
        form = NewUserForm(request.POST or None)
    
        if request.method == "POST" and form.is_valid():
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

@login_required(login_url='/accounts/login/')
def profile(request, username):
    #username = request.data['username']
    # profile = get_object_or_404(User,pk=pk)
    # profile.save()
    user = get_object_or_404(User, username=username)
    
    context = {
        'user': user,

    }
    return render(request,'profile/profile.html', context)

@login_required(login_url='/accounts/login/')
def update_profile(request, username):
    user = get_object_or_404(User, username=username)


    if request.method == 'POST':
        user_form = ExistingUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
                messages.error(request,'Please try updating your profile again.')
    else:
        user_form = ExistingUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,'profile/update_profile.html',{"user_form": user_form, "profile_form":profile_form})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'query' in request.GET and request.GET['query']:
        search_term = request.GET.get('query')
        # searched_query = Neighborhood.find_neighborhood(search_term)
        searched_business = Business.objects.filter(name__icontains=search_term)
        searched_post = Post.objects.filter(post__icontains=search_term)
        
        message = f"{search_term, searched_business, searched_post}"
        
        results = chain(searched_business, searched_post)
        
        params = {
            'message': message,
            'results': results,
            'businesses': searched_business,
            'posts': searched_post,
        }
        
        return render(request, 'search/search.html', params)
    else:
        message = "You haven't searched for any term"
        return render(request, 'search/search.html', {"message": message})

@login_required(login_url='/accounts/login/')               
def neighborhood(request):
    neighborhoods = Neighborhood.objects.all()
    if request.method == 'POST':
        form = NeighborhoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('neighborhood')
        
    else:
        form = NeighborhoodForm()
    
    params = {
        'neighborhoods': neighborhoods,
        'form': form,
    }
    return render(request, 'hood.html', params)



@login_required(login_url='/accounts/login/')
def businesses(request, neighborhood_id):
    # neighborhood_name = Neighborhood.objects.get(id=neighborhood_id)
    neighborhood = get_object_or_404(Neighborhood, pk=neighborhood_id)
    businesses = Business.objects.filter(neighborhood=neighborhood)
    
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('businesses', neighborhood.id)
        
    else:
        form = BusinessForm()
    
    params = {
        'businesses': businesses,
        'form': form,
        # 'neighborhood_name': neighborhood_name,
    }
    return render(request, 'businesses.html', params)