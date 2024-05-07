from rest_framework import serializers
from django.core.validators import URLValidator
from watchlist_app.models import *

class StreamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamingPlatform
        fields = "__all__"

    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return name
    
    def validate(self, instance):
        name = instance.get('name')
        if WatchList.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already exists")
        return instance
    
    def validate_url(self, url):
        validator = URLValidator()
        try:
            validator(url)
        except:
            raise serializers.ValidationError("Invalid URL")
        return url



class WatchListserializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = "__all__"
    
    def get_len_name(self, object):
        return len(object.title)
    
    def validate_title(self, title):
        if len(title) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")
        return title
    
    def validate(self, instance):
        title = instance.get('title')
        if WatchList.objects.filter(title=title).exists():
            raise serializers.ValidationError("Title already exists")
        return instance

""" below is all serializer.Serializer class srializer.

def name_length(vlaue):
    if len(vlaue) >6 :
        raise serializers.ValidationError("Name must be at maximum 6 characters")
    return vlaue
class Movieserializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        print(instance.name , instance.description, instance.active)
        instance.save()
        return instance
    
    def validate_name(self, name):
        if len(name) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        return name
    
    def validate(self, instance):
        name = instance.get('name')
        if Movie.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already exists")
        return instance
    
"""
