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
from django.contrib.auth.forms import AuthenticationForm
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
    save_username_changes,
    save_average_rating_changes,
    display_default_value_for_unrated_videos,
    display_default_value_for_unrated_video,
    set_number_of_ratings,
    set_thumbnail_picture
)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

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
            user = form.save(commit=False)
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


@login_required(login_url='/login/')
def home_view(request):
    all_videos = Video.objects.all()
    all_videos = set_average_rating(all_videos)
    save_average_rating_changes(all_videos)
    highest_rated_video = all_videos.order_by('-average_rating').first()

    videos_by_category = []

    film_and_animation_videos = Video.objects.filter(
        category='Film & Animation')
    videos_by_category.append(film_and_animation_videos)

    autos_and_vehicles_videos = Video.objects.filter(
        category='Autos & Vehicles')
    videos_by_category.append(autos_and_vehicles_videos)

    music_videos = Video.objects.filter(category='Music')
    videos_by_category.append(music_videos)

    pets_and_animals_videos = Video.objects.filter(category='Pets & Animals')
    videos_by_category.append(pets_and_animals_videos)

    sport_videos = Video.objects.filter(category='Sports')
    videos_by_category.append(sport_videos)

    travel_and_events_videos = Video.objects.filter(category='Travel & Events')
    videos_by_category.append(travel_and_events_videos)

    gaming_videos = Video.objects.filter(category='Gaming')
    videos_by_category.append(gaming_videos)

    people_and_blogs_videos = Video.objects.filter(category='People & Blogs')
    videos_by_category.append(people_and_blogs_videos)

    comedy_videos = Video.objects.filter(category='Comedy')
    videos_by_category.append(comedy_videos)

    entertainment_videos = Video.objects.filter(category='Entertainment')
    videos_by_category.append(entertainment_videos)

    news_and_politics_videos = Video.objects.filter(category='News & Politics')
    videos_by_category.append(news_and_politics_videos)

    how_to_and_style_videos = Video.objects.filter(category='Howto & Style')
    videos_by_category.append(how_to_and_style_videos)

    education_videos = Video.objects.filter(category='Education')
    videos_by_category.append(education_videos)

    science_and_technology_videos = Video.objects.filter(
        category='Science & Technology')
    videos_by_category.append(science_and_technology_videos)

    nonprofits_and_activism_videos = Video.objects.filter(
        category='Nonprofits & Activism')
    videos_by_category.append(nonprofits_and_activism_videos)

    for collection in videos_by_category:
        set_thumbnail_picture(collection)
        display_default_value_for_unrated_videos(collection)

    return render(request, 'videoflix/home.html', {
        'all_videos': all_videos,
        'highest_rated_video': highest_rated_video,
        'film_and_animation_videos': film_and_animation_videos,
        'autos_and_vehicles_videos': autos_and_vehicles_videos,
        'music_videos': music_videos,
        'pets_and_animals_videos': pets_and_animals_videos,
        'sport_videos': sport_videos,
        'travel_and_events_videos': travel_and_events_videos,
        'gaming_videos': gaming_videos,
        'people_and_blogs_videos': people_and_blogs_videos,
        'comedy_videos': comedy_videos,
        'entertainment_videos': entertainment_videos,
        'news_and_politics_videos': news_and_politics_videos,
        'how_to_and_style_videos': how_to_and_style_videos,
        'education_videos': education_videos,
        'science_and_technology_videos': science_and_technology_videos,
        'nonprofits_and_activism_videos': nonprofits_and_activism_videos
    })


@login_required(login_url='/login/')
def my_videos(request):
    my_videos = Video.objects.filter(creator=request.user)
    display_default_value_for_unrated_videos(my_videos)
    set_thumbnail_picture(my_videos)

    return render(request, 'videoflix/my-videos.html', {'my_videos': my_videos})


@login_required(login_url='/login/')
def see_top_rated_videos(request):
    videos = Video.objects.all()
    top_rated_videos = videos.order_by('-average_rating')[0:10]
    display_default_value_for_unrated_videos(top_rated_videos)
    set_thumbnail_picture(top_rated_videos)

    return render(request, 'videoflix/top-rated.html', {'top_rated_videos': top_rated_videos})


@login_required(login_url='/login/')
def create_video(request):
    if request.method == "POST":
        form = NewVideoForm(request.POST, request.FILES)

        if form.is_valid():
            save_new_video(request, form)

            return redirect_to_home(request)

    form = NewVideoForm()

    return render(request, 'videoflix/create-video.html')


@login_required(login_url='/login/')
def rate_video(request, pk):
    video_to_rate = Video.objects.get(pk=pk)
    user_ratings_for_this_video = Rating.objects.filter(
        author=request.user, video=video_to_rate)

    if request.method == "POST":
        delete_user_ratings_if_already_exist(user_ratings_for_this_video)
        form = RateVideoForm(request.POST)

        if form.is_valid():
            save_new_user_rating(request, form, video_to_rate)

            return redirect_to_home(request)

    form = RateVideoForm()

    return render(request, 'videoflix/rate-video.html', {'video': video_to_rate})


@login_required(login_url='/login/')
def see_video_details(request, pk):
    video_to_display = Video.objects.get(pk=pk)
    display_default_value_for_unrated_video(video_to_display)

    return render(request, 'videoflix/video-details.html', {'video': video_to_display})


@login_required(login_url='/login/')
def edit_video(request, pk):
    video_to_edit = Video.objects.get(pk=pk)

    if request.method == "POST":
        form = EditVideoForm(request.POST)

        if form.is_valid():
            save_changes(request, video_to_edit, form)

            return redirect_to_home(request)

        else:
            error_response_after_video_edition_attempt(request, video_to_edit)

    form = EditVideoForm()

    return render(request, 'videoflix/edit-video.html', {'video_to_edit': video_to_edit})


@login_required(login_url='/login/')
def delete_video(request, pk):
    video_to_delete = Video.objects.get(pk=pk)

    if request.method == "POST":

        if video_to_delete.creator == request.user:
            video_to_delete.delete()
            messages.success(request, 'You have successfully deleted the video "{}"!'.format(
                video_to_delete.title))

            return redirect_to_home(request)

        else:
            messages.error(
                request, 'Sorry, you cannot delete videos uploaded by other users.')

            return redirect_to_home(request)

    return render(request, 'videoflix/delete-video.html', {'video_to_delete': video_to_delete})


@login_required(login_url='/login/')
def see_summary(request):
    videos = Video.objects.all()
    display_default_value_for_unrated_videos(videos)
    set_number_of_ratings(videos)

    return render(request, 'videoflix/summary.html', {'videos': videos})


@login_required(login_url='/login/')
def edit_user(request):
    user = request.user

    if request.method == "POST":
        form = EditUserForm(request.POST)

        if form.is_valid():
            save_username_changes(user, form, request)

            return redirect_to_home(request)

        else:
            messages.error(
                request, "Unfortunately this username is already in use.")

            return render(request, 'auth/edit-user.html')

    form = EditUserForm()

    return render(request, 'auth/edit-user.html')


@login_required(login_url='/login/')
def delete_account(request):
    user = request.user

    if request.method == "POST":
        user.delete()
        messages.success(
            request, "You have successfully deleted your account. We hope to see you again soon on our platform!")

        return redirect_to_home(request)

    return render(request, 'auth/delete-account.html')


@login_required(login_url='/login/')
def log_out(request):
    logout(request)
    messages.success(
        request, "You have successfully logged out. See you soon!")

    return redirect_to_home(request)


def redirect_to_home(request):
    response = redirect('/home/')

    return response
