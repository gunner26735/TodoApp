from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('t_id','t_title')
        model = models.tag


class TodoTagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        fields = ('todo_id','tag_id','tag')
        model = models.todo_tags


class TodoSerializer(serializers.ModelSerializer):
    tags = TodoTagSerializer(many=True,read_only=True)

    class Meta:
        fields = (
            "id",
            "timestamp",
            "title",
            "description",
            "due_date",
            "status",
            'tags',
            'todo',
        )
        model = models.todo
