
"""
Helper function for the notes app that helps format the grid of notes
"""
def format3(items, row=3):
    PERROW = row
    items2d = []
    for i in range(len(items)):
        if(i%PERROW == 0):
            items2d.append([])
        items2d[-1].append(items[i])
    return items2d


"""
Helper function for the ntoes app that is the search alorithem for note searching

At the momemt it is a simple search that searches for the text in the title or text of the note
But in the future this can be improved to be a more complex search algorithm
"""
def searchEngine(notes, text):
    found = []
    for note in notes:
        if text in note["title"] or text in note["text"]:
            found.append(note)
    return found

"""
Helper function for the ntoes app that is the search alorithem for folder searching

See note in the searchEngine documentation for more details
"""
def searchFolder(folders, text):
    found = []
    for folder in folders:
        if(text in folder["title"]):
            found.append(folder)

    return found

"""
Helper function for the ntoes app that helps retrive the profile picture of a user
"""
def getProfilePictureURL(user):
    try:
        image_url = user.profile.profilePicture.url if user.profile.profilePicture else "/media/profile_pictures/default.png"
    except:
        image_url = "/media/profile_pictures/default.png"
    return image_url