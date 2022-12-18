from django.shortcuts import render, redirect
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user_model
from .forms import NewUserForm, NewVideoForm, EditVideoForm, RateVideoForm, EditUserForm
from .models import Video, Rating
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.messages import get_messages
from .utils import (
    authenticate_user_from_form, 
    success_response_after_login, 
    error_response_after_login_attempt, 
    error_response_after_signup_attempt, 
    send_email, 
    find_encrypted_user, 
    success_response_after_signup, 
    error_response_after_activation_link_expires,
    save_new_video, 
    save_changes,
    error_response_after_video_edition_attempt,
    set_average_rating,
    delete_user_ratings_if_already_exist,
    save_new_user_rating,
    save_username_changes
)
from django.contrib.auth.forms import AuthenticationForm

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def redirect_to_home(request):
    response = redirect('/home/')
    
    return response


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = authenticate_user_from_form(form)
            login(request, user)
            success_response_after_login(request)

            return redirect_to_home(request)

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
        storage = get_messages(request)
        videos = Video.objects.all()

        return render(request, 'videoflix/home.html', {'messages': storage, 'videos': videos})

    else:
        error_response_after_activation_link_expires(request)
        storage = get_messages(request)

        return render(request, 'auth/login.html', {'messages': storage})


@login_required(login_url = '/login/')
def home_view(request):
    videos = Video.objects.all()
    videos = set_average_rating(videos)
    
    return render(request, 'videoflix/home.html', {'videos': videos})


@login_required(login_url = '/login/')
def my_videos(request):
    videos = Video.objects.filter(creator = request.user)
    videos = set_average_rating(videos)
    
    return render(request, 'videoflix/my-videos.html', {'videos': videos})


@login_required(login_url = '/login/')
def see_top_rated_videos(request):
    videos = Video.objects.all()
    videos = set_average_rating(videos)
    # videos = videos.order_by('-average_rating')[0:5]
    
    return render(request, 'videoflix/top-rated.html', {'videos': videos})


@login_required(login_url = '/login/')
def create_video(request):
    if request.method == "POST":
        form = NewVideoForm(request.POST, request.FILES)
        
        if form.is_valid():
            save_new_video(request, form)

            return redirect_to_home(request)

    form = NewVideoForm()

    return render(request, 'videoflix/create-video.html')


@login_required(login_url = '/login/')
def rate_video(request, pk):
    video_to_rate = Video.objects.get(pk = pk)
    user_ratings_for_this_video = Rating.objects.filter(author = request.user, video = video_to_rate)

    if request.method == "POST":
        delete_user_ratings_if_already_exist(user_ratings_for_this_video)
        form = RateVideoForm(request.POST)
        
        if form.is_valid():
            save_new_user_rating(request, form, video_to_rate)

            return redirect_to_home(request)

    form = RateVideoForm()

    return render(request, 'videoflix/rate-video.html', {'video': video_to_rate})


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
            save_changes(request, video_to_edit, form)
            
            return redirect_to_home(request)

        else:
            error_response_after_video_edition_attempt(request, video_to_edit)

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


@login_required(login_url = '/login/')
def edit_user(request):
    user = request.user

    if request.method == "POST":
        form = EditUserForm(request.POST)

        if form.is_valid():
            save_username_changes(user, form, request)
            
            return redirect_to_home(request)

        else:
            messages.error(request, "Unfortunately this username is already in use.")

            return render(request, 'auth/edit-user.html')

    form = EditUserForm()

    return render(request, 'auth/edit-user.html')


@login_required(login_url = '/login/')
def delete_account(request):
    user = request.user

    if request.method == "POST":
        user.delete()
        messages.success(request, "You have successfully deleted your account.")

        return redirect_to_home(request)

    return render(request, 'auth/delete-account.html')


@login_required(login_url = '/login/')
def log_out(request):
    logout(request)
    messages.success(request, "You have successfully logged out. See you soon!")

    return redirect_to_home(request)
