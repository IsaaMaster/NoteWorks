from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="home"), 
    path("notes/<int:folder_id>/", views.notes, name="notes"),
    path("notes/<int:folder_id>/<str:sort>/", views.notes, name="notesSorted"),
    path("note/<int:note_id>/", views.detail, name="detail"),
    path("notes/<int:folder_id>/newNote", views.createNewNote, name="newNote"),
    path("notes/<int:folder_id>/newFolder", views.createNewFolder, name="newFolder"),   
    path("login", views.loginpage, name="loginpage"),
    path("userlogintrue", views.user_login, name="userlogin"), 
    path("register", views.user_registration, name='register'),
    path("save/<int:note_id>/", views.saveNote, name="save"),
    path("search/", views.search, name="search"), 
    path("delete/<int:note_id>/", views.delete, name="delete"),
    path('account/', views.account, name='account'), 
    path('update_account/', views.update_account, name='update_account'), 
    path('sharednotes/', views.sharedNotes, name='sharedNotes'),
    path('share/<int:note_id>/', views.share, name='share'),
    path('download/<int:note_id>/', views.downloadPDF, name='downloadPDF'),
    path("background/<int:folder_id>/<str:background>/", views.changeBackground, name="backgroundChange"),
]
