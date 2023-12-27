from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class todo(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateField(auto_now_add=True,editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    due_date = models.DateField(blank=True,null=True)

    #Choices model for status field
    class StatusChoice(models.TextChoices):
        OPEN = 'OPEN', _('open')
        WORKING = 'WORKING', _('working')
        DONE = 'DONE', _('done')
        OVERDUE = 'OVERDUE', _('overdue')

    status = models.CharField(max_length=10,choices=StatusChoice.choices,default=StatusChoice.OPEN)

class tag(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_title = models.CharField(max_length=20,unique=True)

class todo_tags(models.Model):
    todo_id = models.ForeignKey(todo,on_delete=models.CASCADE)
    tag_id = models.ForeignKey(tag,on_delete=models.CASCADE)