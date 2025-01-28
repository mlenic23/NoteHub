from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),       
    path('add/', views.add_note, name='add_note'), 
    path('<int:note_id>/', views.detail, name='detail'),
    path('<int:note_id>/results/', views.results, name='results'),
    path('<int:note_id>/like/', views.like, name='like'),
]




