from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),       
    path('add/', views.add_note, name='add_note'), 
    path('<int:note_id>/', views.detail, name='detail'),
    path('<int:note_id>/comment/', views.add_comment, name='add_comment'),
   # path('<int:note_id>/results/', views.results, name='results'),
    path('<int:note_id>/like/', views.like, name='like'),
    path('<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('mark_note_important/<int:note_id>/', views.mark_note_important, name='mark_note_important'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('<int:note_id>/lock/', views.lock_note, name='lock_note'),
    path('lock/<int:note_id>/', views.lock_note, name='lock_note'),  
    path('locked_notes/<int:user_id>/', views.locked_notes, name='locked_notes'), 
    path('view_locked/<int:note_id>/', views.view_locked_note, name='view_locked_note'),  
    path('toggle-theme/', views.toggle_theme, name="toggle_theme"),
]




