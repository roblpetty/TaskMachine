from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

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
    completable = models.BooleanField(blank=False,default=True)
    #complete_date = models.DateField(choices=choices)
    optional = models.BooleanField(choices=choices,default=False)

    class Meta:
        unique_together = ('author', 'title')

    def __str__(self):
        return self.title

    def setCompletable(self, delete_id=None):
        incomplete_children = self.children.filter(complete=False,optional=False)
        if delete_id:
            incomplete_children = incomplete_children.exclude(pk=delete_id)
        qs = Post.objects.filter(id=self.id)
        if incomplete_children.count() > 0:
            qs.update(complete=False,completable=False)
        else:
            qs.update(completable=True)

    @property
    def overdue(self):
        if self.due_date is None:
            return False
        else:
            return self.due_date < date.today()

    @property
    def level(self):
        has_child = self.children.count() > 0
        has_parent = Post.objects.filter(children__id=self.id).count() > 0
        if has_child and has_parent:
            return 'mid'
        elif not has_child and has_parent:
            return 'bottom'
        elif has_child and not has_parent:
            return 'top'
        else:
            return 'both'
