from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Post
from django.contrib import messages

@receiver(post_save, sender=Post)
def save_post(sender, instance, **kwargs):
    print(kwargs)
    for task in Post.objects.filter(children__pk=instance.pk):
        Post.setCompletable(task)

@receiver(pre_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    for task in Post.objects.filter(children__pk=instance.pk):
        Post.setCompletable(task,instance.pk)

        