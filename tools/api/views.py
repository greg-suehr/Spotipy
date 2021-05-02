from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from tools.models import User, Library, Playlist
from .serializers import PlaylistSerializer


# @api_view(['GET','POST'])
# class Playlists(request):
#    if request.method == 'GET':
#
#        pass
#    elif request.method == 'POST':
#        pass


class UserRegisterView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    pass


class MyPlaylistsView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
        List all the authenticated user's playlists.
        '''
        playlists = Playlist.objects.filter(user = "gsuehr")
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        '''
        Do something!
        '''
        data = {
#            "uri": "spotify:playlist: bbbb",
#            "user": "gsuehr",
#            "name": "goblin p2",
#           "created": "2021-04-02T00:00"
            "uri": request.POST.get("uri"),
            "user": request.POST.get("user"),
            "name": request.POST.get("name"),
            "created": request.POST.get("created")
        }
        serializer = PlaylistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
