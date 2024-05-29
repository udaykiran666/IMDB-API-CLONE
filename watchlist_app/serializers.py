from rest_framework import serializers
from watchlist_app.models import *

class ReviewsSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        # fields = '__all__'
        exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
    
     
    def validate(self, instance):
        title = instance.get('title')
        if WatchList.objects.filter(title=title).exists():
            raise serializers.ValidationError("Title already exists")
        return instance

class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"

    def validate(self, instance):
        name = instance.get('name')
        if StreamingPlatform.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already exists")
        return instance
