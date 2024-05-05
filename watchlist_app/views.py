from watchlist_app.models import *
from watchlist_app.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def movie_list(request):
    query_set = Movie.objects.all()
    serializer = Movieserializer(query_set, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, pk):
    query_set = Movie.objects.get(id=pk)
    serializer = Movieserializer(query_set)
    return Response(serializer.data)