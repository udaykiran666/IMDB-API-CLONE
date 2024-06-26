from django.http import Http404
from django.shortcuts import get_object_or_404
from watchlist_app.models import *
from watchlist_app.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import *

# for apiview(it is get,post,put,delete)
#
class WatchListAV(APIView):
    def get_query_set(self):
        return WatchList.objects.all()

    def get(self, request):
        try:
            query_set = self.get_query_set()
            serializer = WatchListSerializer(query_set, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
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
            serializer = WatchListSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WatchList.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        serializer = WatchListSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_query_set().get(pk=pk)
        instance.delete()
        return Response({"message": "Deleted Successfully."}, status=status.HTTP_200_OK)

# class StreamingPlatformAV(APIView):
#     def get_query_set(self):
#         return StreamingPlatform.objects.all()
    
#     def get(self, request):
#         try:
#             query_set = self.get_query_set()
#             serializer = StreamingPlatformSerializer(query_set, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except StreamingPlatform.DoesNotExist:
#             raise Http404
        
#     def post(self, request):
#         serializer = StreamingPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class StreamingPlatformDV(APIView):
#     def get_query_set(self):
#         return StreamingPlatform.objects.all()
    
#     def get(self, request, pk):
#         try:
#             instance = self.get_query_set().get(pk=pk)
#             serializer = StreamingPlatformSerializer(instance)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except StreamingPlatform.DoesNotExist:
#             raise Http404
        
#     def put(self, request, pk):
#         instance = self.get_query_set().get(pk=pk)
#         serializer = StreamingPlatformSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         instance = self.get_query_set().get(pk=pk)
#         instance.delete()
#         return Response({"message": "Deleted Successfully."}, status=status.HTTP_200_OK)
    
# viewsets.ViewSet

# class StreamingPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamingPlatform.objects.all()
#         instance = get_object_or_404(queryset, pk=pk)
#         serializer = StreamingPlatformSerializer(instance)
#         return Response(serializer.data)
    
class StreamingPlatformVS(viewsets.ModelViewSet):
    queryset = StreamingPlatform.objects.all()
    serializer_class = StreamingPlatformSerializer

class ReviewCreate(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        user = self.request.user
        review_exists = Reviews.objects.filter(watchlist=watchlist, review_user=user)
        if review_exists.exists():
            raise ValidationError("You have already reviewed this movie.")
        
        if watchlist.total_reviews == 0:
            watchlist.average_rating = serializer.validated_data['rating']
        else:
            watchlist.average_rating = (watchlist.average_rating + serializer.validated_data['rating'])/2

        watchlist.total_reviews = watchlist.total_reviews + 1
        print('average rating: %s' % watchlist.average_rating)
        print('total reviews: %s' % watchlist.total_reviews)
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=user)

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewsSerializer
    # permission_classes = [IsAuthenticated] # for object based permissions
    permission_classes = [IsAuthenticated] # for object based permissions & this means authenyticated users can edit ,acces..unaunthenticated users can only read them.

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Reviews.objects.filter(watchlist=pk)      

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    # permission_classes = [IsAuthenticated] # for object based permissions
    permission_classes = [AdminOrReadOnly] # for object based permissions & this means authenyticated users can edit ,acces..unaunthenticated users can only read them.

    def perform_destroy(self, instance):
        watchlist = instance.watchlist

        watchlist.total_reviews -=1
        if watchlist.total_reviews > 0:
            current_total_rating = watchlist.average_rating * watchlist.total_reviews
            updated_total_rating = current_total_rating - instance.rating
            watchlist.average_rating = updated_total_rating / watchlist.total_reviews
        else:
            # If there are no reviews left, reset the average rating to 0
            watchlist.average_rating = 0

        # Save the updated WatchList object
        watchlist.save()

        # Delete the review
        instance.delete()
 