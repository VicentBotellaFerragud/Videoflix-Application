from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.views.decorators.cache import cache_page
from .forms import NewUserForm, NewVideoForm, EditVideoForm
from .models import Video
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.messages import get_messages
from .utils import authenticate_user_from_form, success_response_after_login, error_response_after_login_attempt, error_response_after_signup_attempt, send_email, find_encrypted_user, success_response_after_signup, error_response_after_activation_link_expires
from django.contrib.auth.forms import AuthenticationForm

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def redirect_to_home(request):
    print('called')
    response = redirect('/home/')
    
    return response

def log_in(request):
    redirect = request.GET.get('next')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = authenticate_user_from_form(form)
            login(request, user)
            # success_response_after_login(request, redirect)
            if redirect:
                messages.success(request, "You have successfully logged in!")
                print(redirect)

                return HttpResponseRedirect(reverse(redirect))

            else:
                messages.success(request, "You have successfully logged in!")
                print('holahola')
    
                redirect_to_home(request)

        else:
            error_response_after_login_attempt(request)

    form = AuthenticationForm()

    return render(request, 'auth/login.html', {'redirect': redirect})


def sign_up(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            send_email(request, user, form.cleaned_data.get('email'))
            storage = get_messages(request)

            return render(request, 'auth/signup.html', {'messages': storage})
        
        else:
            error_response_after_signup_attempt(request, form.errors)

    form = NewUserForm()
    
    return render(request, 'auth/signup.html')


def activate_user(request, uidb64, token):
    User = get_user_model()
    user = find_encrypted_user(User, uidb64)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        success_response_after_signup(request)

    else:
        error_response_after_activation_link_expires(request)


@login_required(login_url = '/login/')
def home_view(request):
    videos = Video.objects.all()
    
    return render(request, 'videoflix/home.html', {'videos': videos})

@login_required(login_url = '/login/')
def create_video(request):

    if request.method == "POST":
        form = NewVideoForm(request.POST, request.FILES)
        
        if form.is_valid():
            instance = form.save(commit = False)
            instance.creator = request.user
            instance.save()
            form = NewVideoForm()
            messages.success(request, "You have successfully added a video!")

            return redirect_to_home(request)

    form = NewVideoForm()

    return render(request, 'videoflix/create-video.html')

@login_required(login_url = '/login/')
def see_video_details(request, pk):

    video_to_display = Video.objects.get(pk = pk)

    return render(request, 'videoflix/video-details.html', {'video': video_to_display})

@login_required(login_url = '/login/')
def edit_video(request, pk):

    video_to_edit = Video.objects.get(pk = pk)

    if request.method == "POST":
        form = EditVideoForm(request.POST)

        if form.is_valid():
            video_to_edit.title = form.cleaned_data.get('title')
            video_to_edit.description = form.cleaned_data.get('description')
            video_to_edit.save()
            form = EditVideoForm()
            messages.success(request, "You have successfully edited the video!")
            
            return redirect_to_home(request)

        else:
            messages.error(request, "Video could not be edited. Please try it again.")
            storage = get_messages(request)

            return render(request, 'videoflix/edit-video.html', {'video': video_to_edit, 'messages': storage})

    form = EditVideoForm()

    return render(request, 'videoflix/edit-video.html', {'video': video_to_edit})

@login_required(login_url = '/login/')
def delete_video(request, pk):

    video_to_delete = Video.objects.get(pk = pk)

    if request.method == "POST":
        video_to_delete.delete()
        messages.success(request, 'You have successfully deleted the video "{}"!'.format(video_to_delete.title))

        return redirect_to_home(request)

    return render(request, 'videoflix/delete-video.html', {'video': video_to_delete})

def log_out(request):
     
    logout(request)
    messages.success(request, "You have successfully logged out. See you soon!")

    return redirect_to_home(request)
