from django.urls import path
from . import views
from .views import (
    PostListView,
    UserPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    ForYouView
)

# This is a list of URL patterns for the 'blog' app.
urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('for-you/', ForYouView.as_view(), name='for-you'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # New URL for the like functionality
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
]
