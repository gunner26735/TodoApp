from rest_framework import serializers
from . import models

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.tag

class TodoTagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = models.todo_tags

class TodoSerializer(serializers.ModelSerializer):
    tags = TodoTagSerializer(read_only=True,many=True)
    class Meta:
        fields = (
            'id',
            'timestamp',
            'title',
            'description',
            'due_date'
        )
        model = models.todo