from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note, Folder
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .helpers import *


def index(request):
    if (request.user.is_authenticated):
        return redirect('notes', folder_id=0)
    return render(request, "app/home.html")


def notes(request, folder_id):
    if not request.user.is_authenticated:
        return redirect('home')
    userfolders = Folder.objects.filter(owner=request.user)
    folder = Folder.objects.filter(id=folder_id)

    if (folder_id != 0 and (len(folder) == 0 or folder[0] not in userfolders)):
        return redirect('home')
    prevFolder = 0
    if (folder_id == 0):
        title = "My Stuff"
    else:
        title = folder.values()[0]["title"]
        prevFolder = folder.values()[0]["folder"]

    notes = Note.objects.filter(
        owner=request.user, folder=folder_id).values().order_by('-lastAccessed')
    folders = Folder.objects.filter(
        owner=request.user, folder=folder_id).values()
    context = {"notes": notes, "prevFolder": prevFolder,
               "folder_title": title, "folder_id": folder_id, "folders": folders}

    return render(request, "app/notes.html", context=context)


def detail(request, note_id):
    if not request.user.is_authenticated:
        return redirect('home')
    userNotes = Note.objects.filter(owner=request.user)
    notes = Note.objects.filter(id=note_id)
    if (len(notes) == 0 or notes[0] not in userNotes):
        return redirect('home')

    for note in notes:
        note.save()
    context = notes.values()[0]

    return render(request, "app/detail.html", context)


def loginpage(request):
    return render(request, 'app/login.html')


def registerpage(request):
    return render(request, 'app/register.html')


def createNewNote(request, folder_id):
    if request.method == 'POST':
        title = request.POST['title']
        if len(title) == 0:
            title = "Unnamed Note"
        note = Note(title=title, text='', owner=request.user, folder=folder_id)
        note.save()
        return redirect('detail', note_id=note.id)
    else:
        return render(request, 'app/newNote.html', context={"folder": folder_id})


def createNewFolder(request, folder_id):
    if request.method == 'POST':
        title = request.POST['title']
        if (len(title) == 0):
            title = "Unnamed Folder"
        folder = Folder(title=title, folder=folder_id, owner=request.user)
        folder.save()
        return redirect('notes', folder_id=folder.id)
    else:
        return render(request, 'app/newFolder.html', context={"folder": folder_id})


def saveNote(request, note_id):
    notes = Note.objects.filter(id=note_id)
    if request.method == 'POST':
        text = request.POST["text"]
        print(request.POST)
        for note in notes:
            note.text = text
            note.save()
    return redirect('notes', folder_id=notes.values()[0]["folder"])


"""
searches the all notes for the search terms

here we use 0 as the folder for the search results
"""
def search(request):
    print(request.method)
    if request.method == 'GET':
        search = request.GET["search"]
        notes = Note.objects.filter(owner=request.user).values()
        folders = Folder.objects.filter(owner=request.user).values()
        notes = searchEngine(notes, search)
        folders = searchFolder(folders, search)
        folder_title = "Search Results for " + "\"" + search + "\""

        return render(request, "app/notes.html", context={"folders": folders, "notes": notes,  "folder_id":0, "prevFolder": 0, "folder_title": folder_title})
    return redirect('home')


def delete(request, note_id):
    notes = Note.objects.filter(id=note_id)
    folder = notes.values()[0]["folder"]
    notes.delete()
    return redirect('notes', folder_id=folder)


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

                #create an example note for the user to see
                note = Note(title='Example Note', text='This is an example Note to help you get started!', owner=user, folder=0)
                note.save()


                # Login the user
                login(request, user)

                # redirect to accounts page:
                return redirect("notes", folder_id=0)

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
            return redirect('notes', folder_id=0)
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'app/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'app/login.html')


def account(request):
    return render(request, 'app/account.html')


@login_required
def update_account(request):
    if request.method == 'POST':
        # get the form data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # update the user's information
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # display a success message
        messages.success(request, 'Your account information has been updated.')

        # redirect the user to the home page
        return redirect('home')

    # if the request method is not POST, render the account page template
    return render(request, 'account.html')
