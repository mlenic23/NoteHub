"""
URL configuration for slikapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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


from images.views import (
    home, 
    index, 
    create_image,
    detail, 
    create_comment,
    profile
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', home, name="homepage"),
    path('slike/', index, name="index"),
    path('slike/create/', create_image, name="create-image"),
    path('slike/<int:id>/', detail, name="detail"),
    path('slike/<int:id>/create-comment/',
         create_comment,
         name="create-comment"),
    path('profile/', profile, name="profile"),
]
