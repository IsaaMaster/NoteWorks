from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from notes.models import Note, Folder
from .serializers import NoteSerializer, FolderSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status

# in progress RESTful API built with Django REST Framework for Noteworks5
# current its very skecky and still needs a lot of work


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/note-list/',
        'Detail View': '/note-detail/<int:id>/',
        'Create Note': '/note-create/',
        'Update Note': '/note-edit/<int:id>/',
        'Delete Note': '/note-delete/<int:id>/',
        'Login': '/user-login/',
        'Logout': '/user-logout/',
        'Folder List': '/folder-list/',
        'Folder Detail': '/folder-detail/<int:id>/',
        'Create Folder': '/folder-create/',
        'Delete Folder': '/folder-delete/<int:id>/',

    }
    return Response(api_urls)


@api_view(['GET'])
def noteList(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def noteDetail(request, id):
    note = Note.objects.get(id=id)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def noteCreate(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def noteEdit(request, id):
    note = Note.objects.get(id=id)
    serializer = NoteSerializer(instance=note, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def noteDelete(request, id):
    note = Note.objects.get(id=id)
    note.delete()
    return Response('Note deleted successfully!')


@api_view(['POST'])
def user_login_view(request):
    if request.method == 'POST':
        from rest_framework.authtoken.serializers import AuthTokenSerializer
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes
@permission_classes
def user_logout_view(request):
    if request.auth:
        request.auth.delete()
        return Response(
            {'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    return Response({'message': 'User not logged in'},
                    status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def folderList(request):
    folders = Folder.objects.all()
    serializer = FolderSerializer(folders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def folderDetail(request, id):
    folder = Folder.objects.get(id=id)
    serializer = FolderSerializer(folder, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def folderCreate(request):
    serializer = FolderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def folderDelete(request, id):
    folder = Folder.objects.get(id=id)
    folder.delete()
    return Response('Folder deleted successfully!')
