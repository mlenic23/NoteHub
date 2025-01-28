from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from .models import Note


def index(request):
    latest_note_list = Note.objects.order_by('-pub_date')[:5]
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