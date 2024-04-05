from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from taggit.serializers import TagListSerializerField, TaggitSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")

    # To encrypt user password in hash
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class TodoSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        fields = (
            "id",
            "timestamp",
            "title",
            "description",
            "due_date",
            "status",
            "tags",
        )
        model = models.todo
