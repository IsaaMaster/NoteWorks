from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Note, Folder, Preferances
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Length
from .helpers import *
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image
from io import BytesIO




def index(request):
    if (request.user.is_authenticated):
        return redirect('notes', folder_id=0)
    return render(request, "app/home.html")


def notes(request, folder_id, sort="date"):
    if not request.user.is_authenticated:
        return redirect('home')

   

    #make sure that user is the owner of the requestd folder
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
        

    if(sort == "title"):
        notes = Note.objects.filter(owner = request.user, folder = folder_id).values().order_by('title')
    elif(sort == "size"):
        notes = Note.objects.filter(owner = request.user, folder = folder_id).values().order_by(-Length('text'))
    elif(sort == "titlereverse"):
        notes = Note.objects.filter(owner = request.user, folder = folder_id).values().order_by('-title')
    else:
        notes = Note.objects.filter(
        owner=request.user, folder=folder_id).values().order_by('-lastAccessed')

    folders = Folder.objects.filter(
        owner=request.user, folder=folder_id).values()
    notesSharedWithUser = Note.objects.filter(sharedUsers = request.user).values()


    context = {"notes": notes, "prevFolder": prevFolder,
               "folder_title": title, "folder_id": folder_id, "folders": folders, "sharedNotes": notesSharedWithUser,
               "background" : request.user.preferances.backgroundImage}

    return render(request, "app/notes.html", context=context)

def sharedNotes(request):
    if not request.user.is_authenticated:
        return redirect('home')
    notesSharedWithUser = Note.objects.filter(sharedUsers = request.user).values()
    #At least for now, there is no shared folders features, so we still show home folders in the shared notes page
    folders = Folder.objects.filter(
        owner=request.user, folder=0).values()
    context=  {"folders": folders, "notes": notesSharedWithUser,  "folder_id":0, "prevFolder": 0, "folder_title": "Notes Shared With Me"}
    
    return render (request, "app/notes.html", context=context); 


def share(request, note_id):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST['username']
        print(username)
        user = User.objects.filter(username=username)
        if (len(user) == 0):
            return redirect('detail', note_id)
        notes = Note.objects.filter(id=note_id)
        if (len(notes) == 0 or notes[0].owner != request.user or str(username) == str(request.user)):
            return redirect('detail', note_id)
        notes[0].sharedUsers.add(user[0])
        notes[0].save()
        return redirect('detail', note_id)

    #notes.sharedUsers.add()

    return redirect('detail', note_id)



def detail(request, note_id):
    if not request.user.is_authenticated:
        return redirect('home')
    userNotes = Note.objects.filter(owner=request.user)
    sharedNotes = Note.objects.filter(sharedUsers=request.user)
    notes = Note.objects.filter(id=note_id)
    if (len(notes) == 0 or (notes[0] not in userNotes and notes[0] not in sharedNotes)):
        return redirect('home')


    for note in notes:
        note.save()
    context = notes.values()[0]

 
    context['sharedUsers'] = notes[0].sharedUsers.all()
    context['background'] = request.user.preferances.backgroundImage


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
        print(request.POST)
        text = request.POST["text"]
        font = request.POST["font"]
        fontSize = request.POST["fontSize"]
        for note in notes:
            note.font = font
            note.fontSize = fontSize
            note.text = text
            note.save()
    return redirect('detail', note_id=note_id)

def changeBackground(request, folder_id, background):
    preferances = request.user.preferances
    preferances.backgroundImage = background
    preferances.save()
    return redirect('notes', folder_id=folder_id)



"""
searches the all notes for the search terms

here we use 0 as the folder for the search results
"""
def search(request):
    #we just redirect to the notes page with the search results. the folder is considerd home (0) with the previous folder being 0
    #this means there won't be a back button to the home page
    if request.method == 'GET':
        search = request.GET["search"]
        notes = Note.objects.filter(owner=request.user).values()
        folders = Folder.objects.filter(owner=request.user).values()
        notes = searchEngine(notes, search)
        folders = searchFolder(folders, search)
        folder_title = "Search Results for " + "\"" + search + "\""
        background = request.user.preferances.backgroundImage

        return render(request, "app/notes.html", context={"folders": folders, "notes": notes,  "folder_id":0, "prevFolder": 0, 
                                                          "background": background, "folder_title": folder_title})
    return redirect('home')


def deleteNote(request, note_id):
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
          
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    'example@gmail.com',
                    form.cleaned_data['password']
                )
            
                #user.first_name = form.cleaned_data['first_name']
                #user.last_name = form.cleaned_data['last_name']
                #user.phone_number = form.cleaned_data['phone_number']
                user.save()

                preferances = Preferances(user=user)
                preferances.save()

                #create an example note for the user to see
                newNoteText = """NoteWorks is a simple note-taking app that brings functional elegance to the next level. Use it to jot down your thoughts, make a to-do list, or take notes for a class all without the distractions of unnecessary features. \r\n\r\n\r\n
This is an example note to get you started! Here are several things to try:\r\n
    - Create a new note or a new folder using the buttons on the home page. If you create a new note and edit it, make sure to save it!\r\n
    - Share a note with a friend using the share button on the right.\r\n
    - Download a PDF of your note to save for later. \r\n
    - Customize your note using the options on the right.\r\n
    - Change the background theme using the customize button on the home page.\r\n"""

                note = Note(title='Welcome to NoteWorks!', text=newNoteText, owner=user, folder=0)
                note.save()


                # Login the user
                login(request, user)

                # redirect to accounts page:
                return redirect("notes", folder_id=0)

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


"""
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
"""


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
    context = {'background': request.user.preferances.backgroundImage}
    return render(request, 'app/account.html', context=context)


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




def downloadPDF(request, note_id):
    userNotes = Note.objects.filter(owner=request.user)
    sharedNotes = Note.objects.filter(sharedUsers=request.user)
    notes = Note.objects.filter(id=note_id)
    if (len(notes) == 0 or (notes[0] not in userNotes and notes[0] not in sharedNotes)):
        return redirect('home')

    note = notes.values()[0]

    buffer = BytesIO()
 

    filename = note['title'] + ".pdf"

    # Create a new PDF object
    pdf = canvas.Canvas(buffer)

    text = note['text'].split("\r\n")

    #Generate the tile of the PDF
    pdf.setFont("Helvetica", 24)
    pdf.drawString(40, 775, note['title'])
    """
    pdf.setFont("Helvetica", 14)
    pdf.drawString(475, 800, "NoteWorks5")
   
    image = ImageReader("./static/app/noteIcon.png")
    img = Image(image, 50, 50)
    img.drawOn(pdf, 420, 800)
    """
    # Generate the content of the PDF
    pdf.setFont("Times-Roman", 12)
    location = 750
    for line in text:
        length = len(line)
        while (length >= 0):
            if(length > 93):
                pdf.drawString(40, location, line[:93])
                line = line[93:]
                length-=93
                location-=15
            else:
                pdf.drawString(40, location, line)
                length-=93
                location-=15
            if(location < 50):
                pdf.showPage()
                location = 750


    

    # Save and close the PDF
    pdf.save()

    # Open the PDF file in binary mode for reading

    buffer.seek(0)

    # Create a FileResponse object with the PDF file
    response = FileResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'
    
    return response



