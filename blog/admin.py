from django.contrib import admin
from .models import Post, Comment

# Register your models here so they appear in the admin interface.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Post model in the admin interface.
    """
    list_display = ('title', 'author', 'publication_date')
    list_filter = ('publication_date', 'author')
    search_fields = ('title', 'content')
    # Automatically fills the author field with the current logged-in user
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Comment model in the admin interface.
    """
    list_display = ('text', 'author', 'post', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('text', 'author__username')

