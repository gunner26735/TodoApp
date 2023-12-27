from django.contrib import admin
from .models import todo,todo_tags,tag

# Register your models here.
admin.site.register(todo)
admin.site.register(todo_tags)
admin.site.register(tag)