"""login URL Configuration

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
from notes.views import social_login_cancelled



urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    # custom override for allauth
    path("accounts/social/login/cancelled/", social_login_cancelled, name="socialaccount_login_cancelled"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/', include('allauth.urls')),
    path('', include('notes.urls')),
]
