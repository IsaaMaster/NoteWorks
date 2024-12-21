from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import Length
from django.http import FileResponse, JsonResponse
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from .models import Note, Folder, Preferances, Profile
from .helpers import searchEngine, searchFolder, getProfilePictureURL, deltaToText, createNewGoogleUser
from .forms import RegisterForm


def index(request):
    """
    This functions manages the home pages for our app, first checking if the user is logged in and
    sending them their home page, else, sending them to their home page
    """
    if (request.user.is_authenticated):

        homeFolder = Folder.objects.filter(owner=request.user, home=True)
        home = None
        message = "None"
        if (len(homeFolder) == 0):
            home = createNewGoogleUser(request.user)
            message = "welcome"
        else:
            home = homeFolder[0]

        return redirect('notesMsg', folder_id=home.id, message = message)
    return render(request, "app/home.html")


@login_required
def notes(request, folder_id, sort="date", message="None"):
    """
    List for all notes that the user owns
    Handles all requests that are related to displaying all notes and folders located within a given folder, including the home folder.
    Has the options for how the content should be sorted upon delivery.
    """
    try:
        folder = Folder.objects.get(id=folder_id)
    except BaseException:
        return redirect('home')

    # makes sure that user is the owner of the requestd folder
    if (not folder or not folder.owner == request.user):
        return redirect('home')

    title = folder.title
    if (not folder.home):
        prevFolder = folder.parent.id
    else:
        prevFolder = -1

    # finds the path of the requested folder for the breadcrumbs on the page
    path = [folder]
    currentFolder = folder
    while (currentFolder.parent is not None):
        path.insert(0, currentFolder.parent)
        currentFolder = currentFolder.parent

    # sorts the notes based on the requested sort methods
    if (sort == "title"):
        notes = Note.objects.filter(
            owner=request.user,
            folder=folder_id).values().order_by('title')
    elif (sort == "size"):
        notes = Note.objects.filter(
            owner=request.user, folder=folder_id).values().order_by(-Length('text'))
    elif (sort == "titlereverse"):
        notes = Note.objects.filter(
            owner=request.user,
            folder=folder_id).values().order_by('-title')
    else:
        notes = Note.objects.filter(
            owner=request.user,
            folder=folder_id).values().order_by('-lastAccessed')

    folders = Folder.objects.filter(
        owner=request.user,
        parent=folder_id).values()

    notesSharedWithUser = Note.objects.filter(
        sharedUsers=request.user).values()

    # context to be passed into the django template
    context = {
        "notes": notes,
        "prevFolder": prevFolder,
        "isHome": folder.home,
        "folder_title": title,
        "folder_id": folder_id,
        "folders": folders,
        "sharedNotes": notesSharedWithUser,
        "background": request.user.preferances.backgroundImage,
        "path": path,
        "message": message,
        "profile_picture": getProfilePictureURL(
            request.user)}

    return render(request, "app/folder.html", context=context)


def detail(request, note_id):
    """
    detail view for a specific note.
    Takes an id for the note and returns the note if the user is the owner of the note.
    else it redirects the user back to the home page
    """
    if not request.user.is_authenticated:
        return redirect('home')
    sharedNotes = Note.objects.filter(sharedUsers=request.user)
    try:
        note = Note.objects.get(id=note_id)
    except BaseException:
        return redirect('home')

    # make sure that the user is the owner of the note or the note has been
    # shared with the user
    if (not note.owner == request.user and note not in sharedNotes):
        return redirect('home')

    # use orginal context
    context = note.__dict__
    context['lastAccessed'] = naturaltime(context['lastAccessed'])
    context['sharedUsers'] = note.sharedUsers.all()
    context['background'] = request.user.preferances.backgroundImage
    context['profile_picture'] = getProfilePictureURL(request.user)

    return render(request, "app/note.html", context)


def sharedNotes(request):
    """
    This function handles the request for the notes that have been shared with the user.
    Similar to the "notes" function, this function returns all notes that have been shared with the user using same template.
    """
    if not request.user.is_authenticated:
        return redirect('home')
    notesSharedWithUser = Note.objects.filter(
        sharedUsers=request.user).values()

    homeFolder = Folder.objects.filter(owner=request.user, home=True)

    # At least for now, there is no shared folders features, so we still show
    # home folders in the shared notes page
    folders = Folder.objects.filter(
        owner=request.user,
        parent=homeFolder[0].id).values()

    context = {
        "folders": folders,
        "notes": notesSharedWithUser,
        "isHome": False,
        "folder_id": homeFolder[0].id,
        "prevFolder": homeFolder[0].id,
        "folder_title": "Notes Shared With Me",
        "background": request.user.preferances.backgroundImage,
        "profile_picture": getProfilePictureURL(
            request.user)}

    return render(request, "app/folder.html", context=context)


def shareNote(request, note_id):
    """
    The function allows users to share notes with other users.
    Handles a note sharing request, given a note_id and a username, which is retrived from the post data.
    This is done by adding the Username to the list of sharedUsers for the note.
    If no username is found, this view does nothing.
    """
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        user = User.objects.filter(username=username)

        # no user with that username found
        if (len(user) == 0):
            return redirect('detail', note_id)
        # tries the retrive the note
        try:
            note = Note.objects.get(id=note_id)
        except BaseException:
            return redirect('detail', note_id)

        # makes sure the owner of the note is the user making the request and
        # makes sure the owner does note share with themselves
        if (note.owner != request.user or str(username) == str(request.user)):
            return redirect('detail', note_id)

        # updates shareUsers and saves changes
        note.sharedUsers.add(user[0])
        note.save()

        return JsonResponse({"success": True})

    return redirect('detail', note_id)


def unshare(request, note_id, username):
    """
    Allows users to unshare notes with other users.
    We prevent the user from unsharing if they are not the owner of the note.
    Otherwise, the user is removed from the list of sharedUsers for that note.
    """
    if not request.user.is_authenticated:
        return redirect('home')

    try:
        note = Note.objects.get(id=note_id)
        user = User.objects.get(username=username)
    except BaseException:
        return redirect('detail', note_id)

    # makes sure the owner of the note is the user making the request
    if (note.owner != request.user):
        return redirect('detail', note_id)

    # updates shareUsers and saves changes
    note.sharedUsers.remove(user)
    note.save()

    return redirect('detail', note_id)


def loginpage(request):
    """
    Renders the login page, where users can login to their account
    """
    return render(request, 'app/login.html')


def registerpage(request):
    """
    Renders the registration page, where users can create a new account
    """
    return render(request, 'app/register.html')


def createNewNote(request, folder_id):
    """
    Handles request to create a new note, given a folder id in which the note will be stored.
    The folder_id argument is the folder in which the new note will be stored in.
    If not name is provided in making the note, it the note will be named "Unnamed Note"
    The first time for the new Note will be the title of the note and will be formatted as a header (see note.js)

    The newNote.html is legacy code, and is not used in the current version of the app.
    Instead of having a whole new page to create a note, we simply use a modal on the notes page to create a new note.
    """
    if request.method == 'POST':
        title = request.POST['title']
        if len(title) == 0:
            title = "Unnamed Note"

        parent = Folder.objects.get(id=folder_id)
        note = Note(title=title, owner=request.user, folder=parent)
        note.save()
        return redirect('detail', note_id=note.id)

    return render(
        request,
        'app/newNote.html',
        context={
            "folder": folder_id})


def createNewFolder(request, folder_id):
    """"
    Handles request to create new folder, given a folder id in which the new folder will be stored.
    The folder_id argument is the folder in which the new folder will be stored in.
    If no name is provided in making the folder, it will be named "Unnamed Folder"

    Similar to create new Note, the newFolder.html is legacy code, and is not used in the current version of the app.
    Instead of having a whole new page to create a folder, we simply use a modal on the notes page to create a new folder.
    """
    if request.method == 'POST':
        title = request.POST['title']
        if (len(title) == 0):
            title = "Unnamed Folder"
        parent = Folder.objects.get(id=folder_id)
        folder = Folder(title=title, parent=parent, owner=request.user)
        folder.save()
        return redirect('notes', folder_id=folder.id)

    return render(
        request,
        'app/newFolder.html',
        context={
            "folder": folder_id})


def saveNote(request, note_id):
    """
    Saves the note given the changes that the user have made to the text, font style, font size, etc.
    Everytime the user makes a change to the note, the note is saved.

    The view simply waits for an AJAX request from the frontend to be made, and then saves the note in real time.
    If the request is faulty, it redirects the user back to the note detail page.
    """
    try:
        note = Note.objects.get(id=note_id)
    except BaseException:
        return redirect('detail', note_id=note_id)

    if request.method == 'POST':
        text = request.POST["text"]
        font = request.POST["font"]
        fontSize = request.POST["fontSize"]
        note.font = font
        note.fontSize = fontSize
        note.text = text
        note.save()
        return JsonResponse({"success": True})

    return redirect('detail', note_id=note_id)


def noteSave(request, note_id):
    """
    Unstable Version:
    New note save function thats compatitable with the new editor: quill
    """
    try:
        note = Note.objects.get(id=note_id)
    except BaseException:
        return redirect('detail', note_id=note_id)

    if request.method == 'POST':
        text = request.POST["text"]
        note.text = text
        note.displayText = deltaToText(text)
        note.save()
        return JsonResponse({"success": True})

    return redirect('detail', note_id=note_id)


def noteGetContents(request, note_id):
    """
    New note retrival function thats compatitable with the new editor: quill
    """
    try:
        note = Note.objects.get(id=note_id)
    except BaseException:
        return redirect('detail', note_id=note_id)

    if request.method == 'GET':
        return JsonResponse({"text": note.text})


def updateNoteFolder(request):
    """
    UpdateNoteFolder allows uses to move a note from one folder to another.

    Currently, users can drag and drop notes into folders, and this function simply handles the AJAX
    requests that are made when a note is dropped into a folder.

    folderID refers to the folder that the note is being moved to, NOT the old folder
    """
    if request.method == 'POST':
        note_id = request.POST["noteID"]
        folder_id = request.POST["folderID"]
        try:
            note = Note.objects.get(id=note_id)
            folder = Folder.objects.get(id=folder_id)
        except BaseException:
            return redirect('home')

        note.folder = folder
        note.save()
        return JsonResponse({"success": True})

    return redirect('home')


@login_required
def changeBackground(request, background):
    """
    Handles the request for changing the background image for the user.

    This view simply handles the AJAX request that is made when the user changes the background image.
    The background image is stored in the user's preferances, and is set to the image that the user has selected.
    """
    if request.method == 'POST':
        background = request.POST['background']
        preferances = request.user.preferances
        preferances.backgroundImage = background
        preferances.save()
        return JsonResponse({"success": True})

    return redirect('home')


@login_required
def renameFolderTitle(request, folder_id):
    """
    Handles the request for renaming a folder and updating the name.

    Takes an AJAX request and updates the folder title to the new title that the user has provided.
    The folder_id is the folder that is being renamed.
    And the new title is the new title that the user has provided in the POST request
    """
    if request.method == 'POST':
        folder = Folder.objects.get(id=folder_id)
        new_title = request.POST['title']
        folder.title = new_title
        folder.save()

        return JsonResponse({"success": True, "new_title": new_title})

    return redirect('notes', folder_id=folder_id)


@login_required
def renameNoteTitle(request, note_id):
    """
    Handles the request for renaming a note and updating the name.

    Takes an AJAX request and updates the note title to the new title that the user has provided.
    The note_id is the note that is being renamed.
    And the new title is the new title that the user has provided in the POST request
    """
    if request.method == 'POST':
        note = Note.objects.get(id=note_id)
        print(request.POST)
        new_title = request.POST['title']
        note.title = new_title
        note.save()
        print(note.title)

        return JsonResponse({"success": True, "new_title": new_title})

    return JsonResponse({"success": False})


@login_required
def search(request):
    """
    Searches the all notes and folders based on a keyword that the user has provided.

    Currently, it just uses helper function searchEngine and searchFolder to search the title of notes and folders and
    the contents of the notes.

    In the future, searchEngine and searchFolder could be improved to provide better search results.


    Here we use 0 as the folder for the search results as a placeholder, which is needed since many tasks (rename folder, delete folder, etc) require a folder id.
    """
    if request.method == 'GET':
        search = request.GET["search"]
        notes = Note.objects.filter(owner=request.user).values()
        folders = Folder.objects.filter(owner=request.user).values()
        notes = searchEngine(notes, search)
        folders = searchFolder(folders, search)
        folder_title = "Search Results for " + "\"" + search + "\""
        background = request.user.preferances.backgroundImage

        homeFolder = Folder.objects.filter(owner=request.user, home=True)
        return render(
            request,
            "app/folder.html",
            context={
                "folders": folders,
                "notes": notes,
                "isHome": False,
                "folder_id": homeFolder[0].id,
                "prevFolder": homeFolder[0].id,
                "profile_picture": getProfilePictureURL(
                    request.user),
                "background": background,
                "folder_title": folder_title})
    return redirect('home')


@login_required
def searchSuggestions(request):
    """
    Handles the AJAX request for search suggestions, given a search keyword.
    """
    if request.method == 'GET':
        keyword = request.GET['keyword']

        # search the title of the notes and folders
        # also makes such the format is parsable by the frontend
        notes = searchEngine(
            Note.objects.filter(
                owner=request.user).values().order_by('-lastAccessed'),
            keyword)[
            :4]
        for note in notes:
            note['time'] = naturalday(note['lastAccessed'])

        folders = searchFolder(
            Folder.objects.filter(
                owner=request.user).values(),
            keyword)[
            :2]

        return JsonResponse(
            {"success": True, "notes": list(notes), "folders": list(folders)})
    return redirect('home')


@login_required
def deleteNote(request, note_id):
    """
    Handles the request for deleting a note, given a note id.

    In order to delete the note, the user must be the owner of the note and the note must exist.

    Once the note it delete, we redirect the user back to the folder that the note was it.
    """
    notes = Note.objects.filter(id=note_id)
    # make sure that the user is the owner of the note
    if (len(notes) == 0 or notes[0].owner != request.user):
        return redirect('home')
    # if the user is the owner of the note, then we can safely delete
    parent = notes.values()[0]["folder_id"]
    notes.delete()
    
    if request.method == 'DELETE':
        return JsonResponse({"success": True})

    if request.method == 'GET':
        return redirect('notes', folder_id=parent)


@login_required
def deleteFolder(request, folder_id):
    """
    Handles the request for deleting a folder, given a folder id. Since in the models we have defined on_delete=models.CASCADE for parent relationships,
    all child notes and folders will be automaticlly deleted.

    In order to delete the folder, the user must be the owner of the folder and the folder must exist.

    Similar to deleting a note, once the folder is delete, we redirect the user back to the folder that the folder was in.
    """
    folder = Folder.objects.get(id=folder_id)
    if (folder.owner != request.user):
        return redirect('home')

    parent = folder.parent.id
    folder.delete()

    return redirect('notes', folder_id=parent)


def user_registration(request):
    """
    Handles the request for a new account, given the post data which contains new user regristration data.
    The username the user has provided must not already exist, and the password and password_repeat must match.

    For now, the user is not required to provide an email, and we use example@gmail.com as a placeholder.

    To create a new account, we create a new user, a new default preferances for the user, and a new default home page.

    We also create a new note, which is an example note to get the user started. Additionaly, provide a welcome message to the user that guides them through using noteworks5
    """
    # if this is a POST request we need to process the form data
    template = 'app/register.html'

    if request.method == 'POST':
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(
                    username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })

            if len(form.cleaned_data['password']) < 8:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Password must be at least 8 characters long.'
                })
            # Create the user:
            user = User.objects.create_user(
                form.cleaned_data['username'],
                'example@gmail.com',
                form.cleaned_data['password']
            )

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # user.first_name = form.cleaned_data['first_name']
            # user.last_name = form.cleaned_data['last_name']
            # user.phone_number = form.cleaned_data['phone_number']
            user.save()

            preferances = Preferances(user=user)
            preferances.save()

            # create a home folder for the user
            homeFolder = Folder(
                title="My Stuff",
                parent=None,
                owner=user,
                home=True)
            homeFolder.save()

            # Login the user
            login(request, user)

            # redirect to accounts page:
            return redirect(
                "notesMsg",
                folder_id=homeFolder.id,
                message="welcome")

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


def user_login(request):
    """
    Handles the request for logging in, given the post data which contains the username and password.
    Currently, we are using Django's built in authentication system, which checks if the username and password combination is correct.
    """
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
            return redirect('home')

        # Incorrect credentials, let's throw an error to the screen.
        return render(request, 'app/login.html',
                      {'error_message': 'Incorrect username and/or password.'})
    # No post data availabe, let's just show the page to the user.
    return render(request, 'app/login.html')


@login_required
def account(request):
    """
    Handles request for the account page, which displays the user's information and allows them to update it.
    """
    numberOfNotes = len(Note.objects.filter(owner=request.user))
    numberOfFolders = len(Folder.objects.filter(owner=request.user))
    favoriteBackground = request.user.preferances.backgroundImage.capitalize()
    friends = 0

    name = request.user.first_name
    if name == '':
        name = request.user.username
       
    context = {
        'background': request.user.preferances.backgroundImage,
        'profile_picture': getProfilePictureURL(
            request.user),
        'numberOfNotes': numberOfNotes,
        'numberOfFolders': numberOfFolders,
        'favoriteBackground': favoriteBackground,
        'friends': friends,
        'name': name}
    return render(request, 'app/account.html', context=context)


@login_required
def update_account(request):
    """
    Handles request for updating the user's account information, given the post data containing the new information.
    The user's username, email, first name, and last name are updated.

    Currently, we do not have support for updating the password, but this can be added in the future.
    """
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
        try:
            user.save()
        except BaseException:
            return JsonResponse({"success": False})

        # display a success message
        messages.success(request, 'Your account information has been updated.')

        # redirect the user to the home page
        return JsonResponse({"success": True})

    # if the request method is not POST, render the account page template

    return render(request, 'account.html')


@login_required
def updateProfilePicture(request):
    """
    Updates the users profile picture
    if the user does not currently have a profile that needs to be updated we create one for them
    """
    if request.method == 'POST':
        # get the form data from the request
        profile_picture = request.FILES.get('profile_picture')

        try:
            profile = Profile.objects.get(user=request.user)
        except BaseException:
            profile = Profile(user=request.user)

        # delete the old profile picture if it exists, so that we do not have
        # to store it
        profile.profilePicture.delete()
        profile.profilePicture = profile_picture
        profile.save()

        # display a success message
        messages.success(request, 'Your profile picture has been updated.')

        # redirect the user to the home page
        return redirect('account')

    # if the request method is not POST, render the account page template
    return render(request, 'account.html')


@login_required
def downloadPDF(request, note_id):
    """
    Handles the request for downloading a note as a PDF, given a note id. Creates a new PDF and draws the specific notes information on it,
    then allows the PDF to be downlaoded by the user.

    The PDF is generated using the reportlab library, which is a python library for generating PDFs.
    """
    userNotes = Note.objects.filter(owner=request.user)
    sharedNotes = Note.objects.filter(sharedUsers=request.user)
    notes = Note.objects.filter(id=note_id)
    if (len(notes) == 0 or (
            notes[0] not in userNotes and notes[0] not in sharedNotes)):
        return redirect('home')

    note = notes.values()[0]

    buffer = BytesIO()

    filename = note['title'] + ".pdf"

    # Create a new PDF object
    pdf = canvas.Canvas(buffer)

    # format text
    text = note['displayText'].split("\n")
    for i in range(len(text)):
        text[i] = text[i].split(" ")

    # Generate the tile of the PDF
    pdf.setFont("Helvetica", 24)
    pdf.drawString(40, 775, note['title'])

    # Generate the author of the note
    user = User.objects.get(id=note['owner_id'])
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, 760, "Author: " + user.username)

    # Generate the content of the PDF
    pdf.setFont("Sans Serif", 12)
    MAX_WIDTH = 500
    y = 735
    for line in text:
        x = 0
        for word in line:
            length = stringWidth(word + " ", "Times-Roman", 12)
            if (length + x >= MAX_WIDTH):
                x = 0
                y -= 15
                if (y < 50):
                    pdf.showPage()
                    y = 750

            pdf.drawString(40 + x, y, word)
            x += length

        y -= 15

    # Save and close the PDF
    pdf.save()

    # Open the PDF file in binary mode for reading

    buffer.seek(0)

    # Create a FileResponse object with the PDF file
    response = FileResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

    return response
