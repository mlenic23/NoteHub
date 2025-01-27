from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse

from .models import Image, Comment

# Create your views here.
def home(request):
    #return HttpResponse("Radi li?!?")
    current_time = timezone.now()
    current_time = current_time.strftime("%H:%M:%S")
    context = {
        'trenutno_vrijeme': current_time
    }
    return render(request, 'images/base.html', context)

def index(request):
    images = Image.objects.all()
    context = {
        'images': images,
    }
    return render(request, 'images/index.html', context)

def create_image(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get('title')
            url = request.POST.get('url')
            if title and url:
                image = Image(
                    title=title,
                    url=url,
                    user = request.user,
                )
                image.save()
                return redirect(
                    reverse('detail', args=(image.id,))
                )
        context = {}
        return render(request, 'images/create.html', context)
    return redirect("/")

def detail(request, id):
    image = get_object_or_404(Image, pk=id)
    #comments = Comment.objects.filter(image=image)
    comments = image.comment_set.all()
    context = {
        'image': image,
        'comments': comments,
    }
    return render(request, 'images/detail.html', context)

def create_comment(request, id):
    image = get_object_or_404(Image, pk=id)
    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST.get('text')
       # user = request.user
        if text:
            comment = Comment(
                text=text,
                user=request.user,
                image=image,
            )
            comment.save()
    return redirect(reverse('detail', args=(image.id,) ))
   

def profile(request):
    user=request.user
    images = user.images_set.all()
    comments = user.comment_set.all()
    return render(request, 'profile.html', {'user': user, 'images': images, 'comments': comments})
