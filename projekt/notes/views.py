from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Note, Comment, PrivateNoteModel
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import NoteForm  
from django.contrib import messages
from accounts.views import is_admin


def index(request):
    search_query = request.GET.get('search', '') 
    order = request.GET.get('order', 'desc') 

    if search_query:
        notes = Note.objects.filter(title__icontains=search_query, is_public= True)
    else:
        notes = Note.objects.filter(is_public = True)

    if request.user.is_authenticated:
         notes = notes | Note.objects.filter(user=request.user, is_private=True)

    if request.user.type == 'REGULARUSER':
        for note in notes:
            if note.user.type == 'SUPERUSER' and note.is_public:
                note.display_role = note.role  
            else:
                note.display_role = None

    if order == 'asc':
        notes = notes.order_by('-is_important', 'pub_date')
    else:
        notes = notes.order_by( '-is_important', '-pub_date') 

    context = {
        'latest_note_list': notes,
        'current_order': order,
        'search_query': search_query,
    }
    return render(request, 'notes/index.html', context)



def home(request):
    return render(request, "notes/home.html")

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    comments = note.comments.all()

    return render(request, 'notes/detail.html', {'note': note, 'comments': comments})


def like(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.likes += 1  
    note.save()  
    return redirect("notes:detail", note_id=note_id) 

@login_required
def add_note(request):

    role_choices = Note.ROLE_CHOICES

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = 'is_public' in request.POST
        is_important = 'is_important' in request.POST and request.user.type == 'SUPERUSER'
        is_private = "is_private" in request.POST
        role = request.POST.get('role', 'personal') if request.user.type == 'SUPERUSER' else None
        category = request.POST.get('category') if request.user.type == 'REGULARUSER' else None


        if not title or not content:
            return HttpResponse("Title and content are required.", status=400)
        
        note = Note.objects.create(
            user=request.user, 
            title=title, 
            content=content, 
            is_public=is_public, 
            is_important=is_important,
            is_private=is_private,
            role=role,
            category=category 
        )
        if request.user.type == 'SUPERUSER':
            if not is_public:
                return redirect('notes:lock_note', note_id=note.id)

        return redirect("notes:index")
    
    return render(request, 'notes/add_note.html', {'role_choices': role_choices})



def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    note.delete()
    
    return redirect('notes:index')  


def add_comment(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if request.method == 'POST':
        text = request.POST.get("comment_text")
        if text:
            Comment.objects.create(note=note, text=text)
    return redirect('notes:detail', note_id=note.id)


@login_required
def mark_note_important(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    if request.user.type == 'SUPERUSER': 
        note.is_important = not note.is_important
        note.save()

        return redirect('accounts:profile', user_id =request.user.id)  
    return HttpResponse("You do not have permission to mark this note.", status=403)

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if note.user != request.user or note.completed:
        return redirect('notes:index')  

    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content') 

        password = request.POST.get('password')
        if password: 
            note.password = password  
            note.is_locked = True  
            note.save()

        return redirect('accounts:profile', user_id=request.user.id)

    return render(request, 'notes/edit_note.html', {'note': note})


@user_passes_test(lambda u: u.is_authenticated and u.type == 'SUPERUSER')
def lock_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if note.user == request.user:
        if request.method == "POST":
            password = request.POST.get('password')
            if password:
                note.password = password
                note.is_locked = True
                note.save()

                return redirect('notes:locked_notes', user_id=request.user.id)  
        return render(request, 'notes/lock_note.html', {'note': note})
    return HttpResponse("You do not have permission to lock this note.", status=403)


def view_locked_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if note.password:
        if request.method == "POST":
            password = request.POST.get('password')
            if password == note.password:
                return render(request, 'notes/detail.html', {'note': note})
            else:
                return HttpResponse("Incorrect password.", status=403)

        return render(request, 'notes/enter_password.html', {'note': note})
    else:
       return render(request, 'notes/detail.html', {'note': note})


def locked_notes(request, user_id):
    if request.user.id != user_id:
        return HttpResponse("You do not have permission to view these notes.", status=403)
    
    locked_notes = Note.objects.filter(user=request.user, is_locked=True)

    context = {
        'locked_notes': locked_notes
    }

    return render(request, 'notes/locked_notes.html', context)


@login_required
def toggle_theme(request):
    if request.method == 'POST':
            if request.session.get('theme') == 'dark':
                request.session['theme'] = 'light'
            else:
                request.session['theme'] = 'dark'

    return redirect('notes:home')  


@login_required
def toggle_completed(request, note_id):
    note = Note.objects.get(id=note_id)
    
    if note.user == request.user and request.user.type == "REGULARUSER":
        note.completed = not note.completed 
        note.save()

    return redirect('notes:index')


@login_required
def profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user == user:
        notes = Note.objects.filter(user=user)
    else:
        notes = Note.objects.filter(user=user, is_public=True)

    return render(request, 'accounts/profile.html', {'profile_user': user, 'notes': notes})

