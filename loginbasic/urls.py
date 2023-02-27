from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="home"), 
    path("notes/", views.notes, name="notes"),
    path("notes/<int:note_id>/", views.detail, name="detail"),
    path("notes/new", views.createNewNote, name="new"),  
    path("login", views.loginpage, name="loginpage"),
    path("userlogintrue", views.user_login, name="userlogin"), 
    path("register", views.user_registration, name='register'),
    path("save/<int:note_id>/", views.saveNote, name="save"),
    path("search/", views.search, name="search")

]
