from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    children = models.ManyToManyField('self',symmetrical=False)
    due_date = models.DateField(blank=True,null=True)
    choices = (
        (True,'Yes'),
        (False,'No'),
    )
    complete = models.BooleanField(blank=False,choices=choices,default=False)
    #complete_date = models.DateField(choices=choices)
    
    optional = models.BooleanField(choices=choices,default=False)

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self):
        return self.title
