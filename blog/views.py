from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Post, UserPostInteraction, Comment
from .forms import PostForm, CommentForm
import joblib
import numpy as np
import os
from django.conf import settings


class PostListView(ListView):
    """
    A view to display a list of all blog posts, with search functionality.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """
        Overrides the default queryset to filter posts based on a search query
        provided in the URL's 'q' parameter.
        """
        query = self.request.GET.get('q')
        if query:
            # Filter posts where the title or content contains the query
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct().order_by('-publication_date')
        else:
            object_list = self.model.objects.all().order_by('-publication_date')
        return object_list


class UserPostListView(ListView):
    """
    A view to display a list of all posts by a specific user.
    """
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-publication_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all().order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.object
            new_comment.author = request.user
            new_comment.save()
            return redirect('post-detail', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object, comment_form=form)
            return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_authenticated:
            UserPostInteraction.objects.get_or_create(user=self.request.user, post=obj)
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ForYouView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/for_you.html'


@login_required
def like_post(request, pk):
    """
    A view to handle liking and unliking a post.
    """
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=pk)


def health_check(request):
    """Simple health check endpoint for deployment debugging"""
    try:
        # Check if database is accessible
        post_count = Post.objects.count()
        
        # Check if media directory exists
        media_exists = os.path.exists(settings.MEDIA_ROOT)
        
        # Check if static files directory exists
        static_exists = os.path.exists(settings.STATIC_ROOT)
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'post_count': post_count,
            'media_directory_exists': media_exists,
            'static_directory_exists': static_exists,
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
