from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        SUPERUSER = "SUPERUSER", "Superuser"
        REGULARUSER = "REGULARUSER", "Regularuser"

    type = models.CharField(
        max_length=20, choices=Types.choices, default=Types.ADMIN
    )

    theme = models.CharField(max_length=10, choices=[("light", "Light"), ("dark", "Dark")], default="light")

    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)

    note = models.TextField(max_length=200, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} - {self.get_type_display()}"
    
    def is_regular_user(self):
        return self.type == self.Types.REGULARUSER