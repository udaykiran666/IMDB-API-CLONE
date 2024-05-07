from django.http import Http404
from watchlist_app.models import *
from watchlist_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class WatchListAV(APIView):
    def get_query_set(self):
        return WatchList.objects.all()

    def get(self, request):
        try:
            query_set = self.get_query_set()
            serializer = WatchListserializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = WatchListserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchDetailDV(APIView):
    def get_query_set(self):
        return WatchList.objects.all()

    def get(self, request, pk):
        try:
            instance = self.get_query_set().get(pk=pk)
            serializer = WatchListserializer(instance)
        except WatchList.DoesNotExist:
            raise Http404
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        serializer = WatchListserializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        instance.delete()
        return Response({"message": "Deleted Successfully."}, status=status.HTTP_200_OK)


class StreamingPlatformAV(APIView):
    def get_query_set(self):
        return StreamingPlatform.objects.all()
    
    def get(self, request):
        try:
            query_set = self.get_query_set()
            serializer = StreamingPlatformSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StreamingPlatform.DoesNotExist:
            return Http404
        
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class StreamingPlatformDV(APIView):
    def query_set(self):
        return StreamingPlatform.objects.all()
    
    def get(self, request, pk):
        try:
            instance = self.query_set().get(pk=pk)
            serializer = StreamingPlatformSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StreamingPlatform.DoesNotExist:
            return Http404
        
    def put(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        serializer = WatchListserializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        instance.delete()
        return Response({"message": "Deleted Successfully."}, status=status.HTTP_200_OK)
