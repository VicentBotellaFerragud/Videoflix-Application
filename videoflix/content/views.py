from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, NewVideoForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Video
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

"""
Redirects the user to the home page.
"""
def redirectToHome(request):

    response = redirect('/home/')
    
    return response

"""
Renders the login view, logs in the user if he/she fulfills the if conditions and redirects him/her either to the home page 
or to the url that he/she has entered.
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
Renders the signup view, signs up the user if he/she fulfills the if conditions and redirects him/her to the login page.
"""
def signupFn(request):

    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            email_sent_notification = activateEmail(request, user, form.cleaned_data.get('email'))
            form = NewUserForm()

            return render(request, 'auth/signup-view.html', {'email_sent_notification': email_sent_notification})

            # return render(request, 'auth/login-view.html', {'signupSuccessful': True})
        
        else:
            return render(request, 'auth/signup-view.html', {'errors': form.errors})

    form = NewUserForm()
    
    return render(request, 'auth/signup-view.html')

def activateEmail(request, user, to_email):

    email_subject = 'Activate your user'
    email_body = render_to_string('auth/activate-user-email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    whole_email = EmailMessage(email_subject, email_body, to = [to_email])

    if whole_email.send():
        email_sent_notification_top = 'Confirmation email was sent to "{}"'.format(to_email)
        email_sent_notification_bottom = 'Click on the link inside to activate your user and finish the signup process'

        return [email_sent_notification_top, email_sent_notification_bottom]

    else:
        email_sent_failure = 'It was not possible to send an email to "{}"'.format(to_email)

        return email_sent_failure

def activate(request, uidb64, token):

    return redirectToHome(request)

"""
Renders the home view and stores in the app the videos the user uploads.
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
Logs out the user and redirects him/her to the home page.
"""
def logoutFn(request):
     
    logout(request)

    return redirectToHome(request)
