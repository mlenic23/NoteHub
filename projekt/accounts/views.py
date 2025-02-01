from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.models import User
from notes.models import Note, Comment, Account
from notes.forms import UserForm, AccountForm, AuthenticationForm
from django.contrib import messages
from accounts.models import CustomUser
from notes.forms import PrivateNoteForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)
      
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.email = user_form.cleaned_data['email']

            user_type = request.POST.get('type', 'REGULARUSER')
            user.type = user_type
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()


            messages.success(request, "Registration successful. Welcome!")
            return redirect('accounts:login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            
    else:
        user_form = UserForm()
        account_form = AccountForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'account_form': account_form})
    

def profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    try:
        account = user.account  # Ispravno: koristi `user.account`
    except Account.DoesNotExist:
        account = None

    regular_user = account.regular_user if account else None
    superuser = account.superuser if account else None

    notes = Note.objects.filter(user=user)

    private_notes = []
    for note in notes:
        private_notes.extend(note.private_notes.all())

    public_notes = notes.filter(is_public=True)

    context = {
        'profile_user': user,
        'account': account,
        'regular_user': regular_user,
        'superuser': superuser,
        'private_notes': private_notes,
        'public_notes': public_notes,
    }

    return render(request, 'accounts/profile.html', context)

    

def logout_view(request):
    logout(request)
    return redirect('home')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        
        if form.is_valid():
            user = form.user
            auth_login(request, user)
            return redirect('accounts:profile', user_id=user.id)  
    
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})