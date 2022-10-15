from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
    
    if request.method == 'POST':
        user = authenticate(username = request.POST['username'], password = request.POST['password'])

        if user:
            login(request, user)

            if redirect:
                return HttpResponseRedirect(request.POST.get('next'))
            
            else:
                return HttpResponseRedirect('/home/')
        
        else:
            return render(request, 'auth/login-view.html', {'wrongPassword': True, 'redirect': redirect})

    return render(request, 'auth/login-view.html', {'redirect': redirect})

"""
Renders the signup view and signs up the user if he/she fulfills the if conditions.
"""
def signupFn(request):
    
    newUsername = request.POST.get('newUsername')
    newPassword = request.POST.get('newPassword')
    repeatPassword = request.POST.get('repeatPassword')

    if request.method == 'POST':
        
        if newUsername != '' and newPassword != '' and repeatPassword !='': 

            if newPassword == repeatPassword: 

                try: 
                    user= User.objects.get(username = newUsername)
                    return render(request, 'auth/signup-view.html', {'usernameAlreadyExists': True})  

                except User.DoesNotExist: 
                    user = User.objects.create_user(username = newUsername, password = newPassword)
                    user.save()
                    return render(request, 'auth/login-view.html', {'signupSuccessful': True})

            else:

                return render(request, 'auth/signup-view.html', {'passwordsDifferent': True})

        else:
            return render(request, 'auth/signup-view.html', {'anyFieldEmpty': True})

    
    return render(request, 'auth/signup-view.html')

"""
Renders the videoflix home view.
"""
@login_required(login_url = '/login/')
def index(request):  
    
    return render(request, 'videoflix/index.html')

"""
Logs out the user and redirects the user to the videoflix home page.
"""
def logoutFn(request):
    
    logout(request)

    response = redirect('/home/')
    
    return response
