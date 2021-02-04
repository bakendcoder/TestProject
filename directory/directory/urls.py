"""directory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from profiles import urls as profile_urls
from generic.forms import CustomAuthForm

from . import views

auth_urls = [
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

apps_urls = [
    path("auth/", include((auth_urls, 'auth'))),
    path("teachers/", include((profile_urls, 'profiles'))),
]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),
    path('directory/', include(apps_urls))
]


# urlpatterns += apps_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)