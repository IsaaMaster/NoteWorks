from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="home"), 
    path("notes/<int:folder_id>/rename_folder/", views.renameFolderTitle, name="renameFolder"),
    path("notes/<int:folder_id>/", views.notes, name="notes"),
    path("note/<int:note_id>/", views.detail, name="detail"),
    path("notes/<int:folder_id>/newNote", views.createNewNote, name="newNote"),
    path("notes/<int:folder_id>/newFolder", views.createNewFolder, name="newFolder"),   
    path("login", views.loginpage, name="loginpage"),
    path("userlogintrue", views.user_login, name="userlogin"), 
    path("register", views.user_registration, name='register'),
    path("note/<int:note_id>/save_note/", views.saveNote, name="save_note"), 
    #path("save/<int:note_id>/", views.saveNote, name="save"), Legacy save method
    path("search/", views.search, name="search"), 
    path("delete/<int:note_id>/", views.deleteNote, name="delete"),
    path('account/', views.account, name='account'), 
    path('update_account/', views.update_account, name='update_account'), 
    path('sharednotes/', views.sharedNotes, name='sharedNotes'),
    #path('share/<int:note_id>/', views.share, name='share'),
    path('note/<int:note_id>/share_note/', views.shareNote, name='share_note'), 
    path('unshare/<int:note_id>/<str:username>', views.unshare, name='unshare'),
    path('download/<int:note_id>/', views.downloadPDF, name='downloadPDF'),
    #path("background/<int:folder_id>/<str:background>/", views.changeBackground, name="backgroundChange"),
    path("background/<str:background>/", views.changeBackground, name="newBackground"),
    path("deleteFolder/<int:folder_id>/", views.deleteFolder, name="deleteFolder"),
    #path("renameFolder/<int:folder_id>/", views.renameFolder, name="renameFolder"),
    path("notes/<int:folder_id>/<str:sort>/", views.notes, name="notesSorted"),
    path("notes/<int:folder_id>/msg/<str:message>/", views.notes, name="notesMsg"),
]
