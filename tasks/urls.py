from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='tasks-home'),
    path('main/', PostListView.as_view(), name='tasks-main'),
    #path('main/<int:id>', PostListView.as_view(), name='tasks-main'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='tasks-about'),
    path('ajax/subtasks/', views.potential_subs, name = 'subtasks'),
    path('ajax/updatesubs/',views.updateSubs, name='updateSubs')
]