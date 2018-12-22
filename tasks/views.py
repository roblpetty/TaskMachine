from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.core import serializers
import datetime
import json

class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'tasks/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        taskId = self.request.GET.get('id')
        UserPosts = Post.objects.filter(author=self.request.user)
        if self.request.GET.get('id') is None or UserPosts.filter(pk=taskId).count() < 1: 
            taskId = UserPosts.first().pk
        else:
            self.request.GET.get('id')
        
        context['post'] = Post.objects.get(pk=taskId)
        return context

    def get_queryset(self, **kwargs):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','due_date','complete','optional','content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all().filter(author=self.request.user)
        taskId = self.request.GET.get('id')
        UserPosts = Post.objects.filter(author=self.request.user)
        if self.request.GET.get('id') is None or UserPosts.filter(pk=taskId).count() < 1: 
            taskId = UserPosts.first().pk
        else:
            self.request.GET.get('id')
        
        context['post'] = Post.objects.get(pk=taskId)
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
    curr_task = request.GET.get('task', None)
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
    fields = ['title','due_date','complete','optional','content']
    #success_url = '/'

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
        taskId = self.request.GET.get('id')
        UserPosts = Post.objects.filter(author=self.request.user)
        if self.request.GET.get('id') is None or UserPosts.filter(pk=taskId).count() < 1: 
            taskId = UserPosts.first().pk
        else:
            taskId = self.request.GET.get('id')
        
        context['post'] = Post.objects.get(pk=taskId)
        context['sublist'] = context['post'].children.all()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/post/'

    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

def about(request):
    return render(request, 'tasks/about.html', {'title': 'About'})