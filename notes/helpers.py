import json
from .models import Folder, Preferances, Profile
from allauth.socialaccount.models import SocialAccount
from django.core.files.base import ContentFile
import requests

# deprecated
def format3(items, row=3):
    """
    Helper function for the notes app that helps format the grid of notes
    """
    PERROW = row
    items2d = []
    for i in range(len(items)):
        if (i % PERROW == 0):
            items2d.append([])
        items2d[-1].append(items[i])
    return items2d





def searchEngine(notes, text):
    """
    Helper function for the notes app that is the search alorithem for note searching

    At the momemt it is a simple search that searches for the text in the title or text of the note
    But in the future this can be improved to be a more complex search algorithm
    """
    text = text.strip()
    found = []
    for note in notes:
        relevant = False
        for word in note["title"].split():
            if text.lower() in word.lower():
                relevant = True
                break
        for word in note["displayText"].split():
            if text.lower() in word.lower():
                relevant = True
                break
        if relevant:
            found.append(note)
    return found





def searchFolder(folders, text):
    """
    Helper function for the ntoes app that is the search alorithem for folder searching

    See note in the searchEngine documentation for more details
    """
    found = []
    for folder in folders:
        for word in folder["title"].split():
            if text.lower() in word.lower():
                found.append(folder)
                break
    return found





def getProfilePictureURL(user):
    """
    Helper function for the ntoes app that helps retrive the profile picture of a user
    """
    try:
        image_url = user.profile.profilePicture.url if user.profile.profilePicture else "/media/profile_pictures/default.png"
    except BaseException:
        image_url = "/media/profile_pictures/default.png"
    return image_url





def deltaToText(noteText):
    """
    Helper function that converts Quill Editor files changes to text
    Needed for the quill editor to work in the frontend
    """
    noteText = json.loads(noteText)
    text = ""
    for ops in noteText['ops']:
        if "insert" in ops:
            text += ops["insert"]

    return text


def createNewGoogleUser(user):
    """
    Helper function that creates a new user in the database
    """
    home = Folder(
        title="My Stuff",
        parent=None,
        owner=user,
        home=True)
    home.save()

    preferances = Preferances(user=user)
    preferances.save()

    social_account = SocialAccount.objects.filter(user=user, provider='google').first()

    if social_account:
        # Get the user's profile picture
        extra_data = social_account.extra_data

        profile_picture = extra_data.get('picture', '')
        response = requests.get(profile_picture, timeout=10)
        profile_picture = ContentFile(response.content, name=f'{user.username}_profile_picture.jpg')

        profile = Profile(user=user, profilePicture=profile_picture)
        profile.save()
    return home