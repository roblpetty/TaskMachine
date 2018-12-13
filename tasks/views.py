from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post


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
    fields = ['title','content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.date_edited = datetime.datetime.utcnow().replace(tzinfo=utc)
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user ==  post.author:
            return True
        return False

def about(request):
    return render(request, 'tasks/about.html', {'title': 'About'})