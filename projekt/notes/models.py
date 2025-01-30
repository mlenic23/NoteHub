import datetime

from django.db import models
from django.utils import timezone
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.note.title} by {self.created_at}"

   