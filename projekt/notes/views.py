from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Note, Comment


def index(request):
    latest_note_list = Note.objects.all()
    context = {'latest_note_list': latest_note_list}
    return render(request, 'notes/index.html', context)

def home(request):
    return render(request, "notes/home.html")

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    comments = note.comments.all()

    return render(request, 'notes/detail.html', {'note': note, 'comments': comments})

#def results(request, note_id):
   # response = "You're looking at the results of note %s."
    # return HttpResponse(response % note_id)

def like(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.likes += 1  
    note.save()  
    return redirect("notes:detail", note_id=note_id) 

def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return HttpResponse("Title and content are required.", status=400)

        Note.objects.create(title=title, content=content)

        return redirect('notes:index') 

    return render(request, 'notes/add_note.html')


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
