from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    path('notes/', views.noteList, name='noteList'),
    path('note/<int:id>/', views.noteDetail, name='noteDetail'),
    path('note-create/', views.noteCreate, name='noteCreate'),
    path('note-edit/<int:id>/', views.noteEdit, name='noteEdit'),
    path('note-delete/<int:id>/', views.noteDelete, name='noteDelete'),
    path('user-login/', views.user_login_view, name='user_login_view'),
    path('user-logout/', views.user_logout_view, name='user_logout_view'),
    path('folders/', views.folderList, name='folderList'),
    path('folder/<int:id>/', views.folderDetail, name='folderDetail'),
    path('folder-create/', views.folderCreate, name='folderCreate'),
    path('folder-delete/<int:id>/', views.folderDelete, name='folderDelete'),

]
