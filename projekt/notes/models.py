import datetime

from django.db import models
from django.utils import timezone
from django.db.models import Q
from accounts.models import CustomUser

class PrivateNoteModel(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Private Note created on {self.created_at}"


class Note(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    private_notes = models.ManyToManyField(PrivateNoteModel, blank=True)
    is_public = models.BooleanField(default=True)
    is_important = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True, blank=True)
    completed = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.note.title} by {self.created_at}"



class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    regular_user = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.user.email}, {self.user.get_type_display()})"
    
