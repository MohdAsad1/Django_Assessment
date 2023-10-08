from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Article, Comment

# Custom admin class for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    search_fields = ('user__username', 'user__email', 'date_of_birth')
    list_per_page = 20

# Custom admin class for Article
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_public')
    list_filter = ('is_public',)
    search_fields = ('title', 'author__username')
    list_per_page = 20

# Custom admin class for Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'content')
    search_fields = ('article__title', 'author__username', 'content')
    list_per_page = 20

# Register your models with the custom admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
