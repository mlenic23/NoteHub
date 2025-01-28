from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Note


def index(request):
    latest_note_list = Note.objects.all()
    context = {'latest_note_list': latest_note_list}
    return render(request, 'notes/index.html', context)

def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'notes/detail.html', {'note': note})

def results(request, note_id):
    response = "You're looking at the results of note %s."
    return HttpResponse(response % note_id)

def like(request, note_id):
    return HttpResponse("You like note %s." % note_id)

def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return HttpResponse("Title and content are required.", status=400)

        Note.objects.create(title=title, content=content)
        return redirect('index') 

    return render(request, 'notes/add_note.html')