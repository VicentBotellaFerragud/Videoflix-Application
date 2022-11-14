from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, NewVideoForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Video

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

"""
Redirects the user to the videoflix home page as soons as the app loads.
"""
def redirectToHome(request):

    response = redirect('/home/')
    
    return response

"""
Renders the login view and logs in the user if he/she fulfills the if conditions.
"""
def loginFn(request):

    redirect = request.GET.get('next')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)

                if redirect:
                    return HttpResponseRedirect(request.POST.get('next'))

                else:
                    return redirectToHome(request)

            else:
                return render(request, 'auth/login-view.html', {'errors': form.errors, 'redirect': redirect})
        else:
            return render(request, 'auth/login-view.html', {'errors': form.errors, 'redirect': redirect})

    form = AuthenticationForm()

    return render(request, 'auth/login-view.html', {'redirect': redirect})

"""
Renders the signup view and signs up the user if he/she fulfills the if conditions.
"""
def signupFn(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            form.save()
            form = NewUserForm()
            return render(request, 'auth/login-view.html', {'signupSuccessful': True})
        
        else:
            return render(request, 'auth/signup-view.html', {'errors': form.errors})

    form = NewUserForm()
    
    return render(request, 'auth/signup-view.html')

"""
Renders the videoflix home view.
"""
@login_required(login_url = '/login/')
# @cache_page(CACHE_TTL) --> This prevents the username from not being updated in the "base.html" file. Why?
def index(request):

    videos = Video.objects.filter(creator = request.user) 

    if request.method == "POST":
        form = NewVideoForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit = False)
            instance.creator = request.user
            instance.save()
            form = NewVideoForm()
            return redirectToHome(request)

    form = NewVideoForm()
    
    return render(request, 'videoflix/index.html', {'videos': videos})

"""
Logs out the user and redirects the user to the videoflix home page.
"""
def logoutFn(request):
     
    logout(request)
    response = redirect('/home/')
    
    return response
