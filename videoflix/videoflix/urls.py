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
from videoflix.content import views

urlpatterns = [
    path('', views.redirectToHome),
    path('login/', views.loginFn, name = 'login'),
    path('signup/', views.signupFn, name = 'signup'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
    path('home/', views.index, name = 'home'),
    path('logout/', views.logoutFn, name = 'logout'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('__debug__/', include('debug_toolbar.urls'), name = 'debug'),
    path('django-rq/', include('django_rq.urls'), name = 'django-rq'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
