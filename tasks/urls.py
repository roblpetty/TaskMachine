from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='tasks-home'),
    path('<int:id>', PostListView.as_view(), name='tasks-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='tasks-about'),
]