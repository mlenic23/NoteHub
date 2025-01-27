from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=160, null=True, blank=True)
    url = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} -> {self.title}"
    
class Comment(models.Model):
    text = models.CharField(max_length=128)
  #  author = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, 
                              on_delete=models.CASCADE
                              )
    def __str__(self):
        return f"{self.id} -> {self.user.username}: {self.text}; slika: {self.image.title}"
    
 
