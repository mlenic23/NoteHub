from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
        path('profile/<int:user_id>', views.profile, name="profile"),
        path('register', views.register, name="register"),
        path('logout/', views.logout_view, name='logout'),
        path('login/', views.login, name='login'),
        path('user_list/', views.user_list, name='user_list'), 
        path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'), 
        path('approve_note/<int:note_id>/', views.approve_note, name='approve_note'),
        path('unapprove/<int:note_id>/', views.unapprove_note, name='unapprove_note'),       
]