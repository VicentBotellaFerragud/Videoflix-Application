from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.messages import get_messages
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .forms import NewVideoForm, EditVideoForm, RateVideoForm
from .models import Video, Rating

# log_in utils:

def authenticate_user_from_form(form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username = username, password = password)
    
    return user


def success_response_after_login(request):
    messages.success(request, "You have successfully logged in!")


def error_response_after_login_attempt(request):
    messages.error(request, "You have entered an invalid username or password.")
    storage = get_messages(request)

    return render(request, 'auth/login.html', {'messages': storage})


# sign_up and activate_user utils:

def send_email(request, user, email):
    email_subject = 'Activate your user'
    email_body = render_to_string('auth/activate-user-email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    whole_email = EmailMessage(email_subject, email_body, to = [email])

    if whole_email.send():
        messages.warning(request, 'Confirmation email was sent to "{}". Please click on the link inside to activate your user and finish the signup process.'.format(email))

    else:
        messages.error('It was not possible to send an email to "{}"'.format(email))


def success_response_after_signup(request):
    messages.success(request, "You have successfully signed up!")


def error_response_after_activation_link_expires(request):
    messages.error(request, "The activation link has expired. Please repeat the whole process from the beginning.")


def error_response_after_signup_attempt(request, errors):
    for error in errors:
        if error == 'username':
                messages.error(request, "Unfortunately this username is already in use.")

        elif error == 'email':
                 messages.error(request, "Please check the email format. It's not correct.")

        else:
            messages.error(request, "Please remember that your password has to be the same in both fields.")

        storage = get_messages(request)

        return render(request, 'auth/signup.html', {'messages': storage})


def find_encrypted_user(user_model, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk = uid)

        return user
    
    except:
        user = None

        return None


# home_view, my_videos and see_top_rated_videos utils:

def set_average_rating(videos):
    for video in videos:
        ratings = Rating.objects.filter(video = video)

        if len(ratings) > 0:
            sum_of_ratings = 0

            for rating in ratings:
                sum_of_ratings += rating.rating
            
            average_rating = sum_of_ratings/len(ratings)
            video.average_rating = "{:.1f}".format(average_rating)

        else:
            video.average_rating = "NR"

    return videos


# create_video utils:

def save_new_video(request, form):
    instance = form.save(commit = False)
    instance.creator = request.user
    instance.save()
    form = NewVideoForm()
    messages.success(request, "You have successfully added a video!")


# rate_video utils:

def delete_user_ratings_if_already_exist(ratings):
    if len(ratings) > 0:
        ratings.delete()


def save_new_user_rating(request, form, video_to_rate):
    rating_as_number = int(form.cleaned_data.get('rating'))
    new_rating = Rating.objects.create(rating = rating_as_number, video = video_to_rate, author = request.user)
    new_rating.save()
    form = RateVideoForm()
    messages.success(request, "You have successfully rated the video!")


# edit_video utils:

def save_changes(request, video_to_edit, form):
    video_to_edit.title = form.cleaned_data.get('title')
    video_to_edit.description = form.cleaned_data.get('description')
    video_to_edit.save()
    form = EditVideoForm()
    messages.success(request, "You have successfully edited the video!")


def error_response_after_video_edition_attempt(request, video_to_edit):
    messages.error(request, "Video could not be edited. Please try it again.")
    storage = get_messages(request)

    return render(request, 'videoflix/edit-video.html', {'video': video_to_edit, 'messages': storage})


# edit_user utils:

def save_username_changes(user, form, request):
    user.username = form.cleaned_data.get('username')
    user.save()
    messages.success(request, "You have successfully edited your username!")
    