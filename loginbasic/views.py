from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
import datetime

from .helpers import *
# Create your views here.

def index(request):
    if (request.user.is_authenticated):
        return redirect('notes')
    return render(request, "app/home.html")

def notes(request):
    if not request.user.is_authenticated:
        return redirect('home')

    notes = Note.objects.filter(owner=request.user).values().order_by('-lastAccessed')
   
  
    context = {"notes": format3(notes)}
    

    return render(request, "app/notes.html", context=context)

def detail(request, note_id):
    if not request.user.is_authenticated:
        return redirect('home')
    notes = Note.objects.filter(id=note_id)
    for note in notes:
        note.save()
    context = notes.values()[0]; 
   
    return render(request, "app/detail.html", context)
def loginpage(request):
    return render(request, 'app/login.html')

def registerpage(request):
    return render(request, 'app/register.html')


def user_registration(request):
    # if this is a POST request we need to process the form data
    template = 'app/register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
               
                # Login the user
                login(request, user)
               
                # redirect to accounts page:
                return redirect("notes")

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect('notes')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'app/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'app/login.html')


def createNewNote(request):
    if request.method == 'POST':
        title = request.POST['title']
        if len(title) == 0:
            title = "unnamed"
        note = Note(title=title, text='', owner = request.user)
        note.save()
        return redirect('detail', note_id = note.id)
    

    else:
        return render(request, 'app/new.html')

def saveNote(request, note_id):
    if request.method == 'POST':
        notes = Note.objects.filter(id=note_id)
        text = request.POST["text"]
        print(request.POST)
        for note in notes:

            note.text = text
            note.save()
    return redirect('notes')        


def search(request):
    print(request.method)
    if request.method == 'GET':
        search = request.GET["search"]
        notes = Note.objects.filter(owner=request.user).values()  
        return render(request, "app/notes.html", context={"notes": format3(searchEngine(notes, search))})
    return redirect('home')

def delete(request, note_id):
    Note.objects.filter(id=note_id).delete()
    return redirect('notes')



