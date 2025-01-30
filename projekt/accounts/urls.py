from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
        path('profile/<int:user_id>', views.profile, name="profile"),
        path('register', views.register, name="register"),
        path('logout/', views.logout_view, name='logout'),
        path('login/', views.login, name='login'),
]