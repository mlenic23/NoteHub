from django.contrib import admin

# Register your models here.
from .models import Note, Comment, Account, PrivateNoteModel

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Account)
admin.site.register(PrivateNoteModel)