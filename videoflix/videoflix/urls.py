"""videoflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from content import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.redirect_to_home),
    path('login/', views.log_in, name = 'login'),
    path('signup/', views.sign_up, name = 'signup'),
    path('activate/<uidb64>/<token>', views.activate_user, name = 'activate'),
    path('logout/', views.log_out, name = 'logout'),
    path('edit-user/', views.edit_user, name = 'edit-user'),
    path('delete-account/', views.delete_account, name = 'delete-account'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('__debug__/', include('debug_toolbar.urls'), name = 'debug'),
    path('django-rq/', include('django_rq.urls'), name = 'django-rq'),
    path('home/', views.home_view, name = 'home'),
    path('my-videos/', views.my_videos, name = 'my-videos'),
    path('top-rated/', views.see_top_rated_videos, name = 'top-rated'),
    path('create-video/', views.create_video, name = 'create-video'),
    path('rate-video/<int:pk>', views.rate_video, name = 'rate-video'),
    path('video-details/<int:pk>', views.see_video_details, name = 'video-details'),
    path('edit-video/<int:pk>', views.edit_video, name = 'edit-video'),
    path('delete-video/<int:pk>', views.delete_video, name = 'delete-video'),
    path('summary/', views.see_summary, name = 'summary'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns() 
