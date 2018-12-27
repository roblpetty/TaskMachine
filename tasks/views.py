from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import CreatePostForm, UpdatePostForm
from django.core import serializers
import datetime
import json
from django.db import IntegrityError
from django.http import HttpResponse

class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'tasks/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        taskId = self.request.GET.get('id')
        UserPosts = Post.objects.filter(author=self.request.user)
        if UserPosts.count() < 1:
            context['post'] = None
            context['sublist'] = None
        elif taskId == 'new' or taskId is None or UserPosts.filter(pk=taskId).count() < 1: 
            taskId = UserPosts.first().pk
            context['post'] = Post.objects.get(pk=taskId)
            context['sublist'] = context['post'].children.all()
        else:
            context['post'] = Post.objects.get(pk=taskId)
            context['sublist'] = context['post'].children.all()
        
        
        
        return context

    def get_queryset(self, **kwargs):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    success_url = '/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        context['post'] = {'pk': 'new'}
        return context

def isAncestor(possible_ancestor,task_id):
    parents = Post.objects.filter(children__pk=task_id).values_list('pk', flat=True)
    if possible_ancestor in parents:
        return True
    elif len(parents) > 0:
        for parentId in parents:
            isAncestor(possible_ancestor,parentId)
    return False

def potential_subs(request):
    curr_task = int(request.GET.get('task', None))
    qs = Post.objects.filter(author=request.user)
    sublist = []
    for item in qs:
        if item.pk != curr_task and not isAncestor(item.pk,curr_task):
            sublist.append(item.pk)
    qs = Post.objects.filter(pk__in=sublist)
    data = serializers.serialize('json',qs)
    return JsonResponse(data, safe=False)

#this is a hack that I need to replace when I learn more how django works
def updateSubs(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        curr_post = Post.objects.get(pk=data['task'])
        if(data['action']):
            curr_post.children.add(Post.objects.get(pk=data['child']))
        else:
            curr_post.children.remove(Post.objects.get(pk=data['child']))
        return JsonResponse("", safe=False)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PostUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        # Assuming there is a ForeignKey from Comment to Post in your model
        return '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        context['sublist'] = context['post'].children.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        return context

def about(request):
    return render(request, 'tasks/about.html', {'title': 'About'})