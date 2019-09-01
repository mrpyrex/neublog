from django.contrib import admin

# Register your models here.
from .models import Post, Comment, PostCategory


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'date', 'active')
    list_filter = ('active', 'date')
    search_fields = ('name', 'email', 'body')
    list_editable = ('active',)


admin.site.register(Comment, CommentAdmin)


class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('cat_title',)}


admin.site.register(PostCategory, PostCategoryAdmin)
