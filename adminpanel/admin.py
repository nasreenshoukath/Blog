from django.contrib import admin
from .models import Profile, Blog, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog', 'created_at', 'is_hidden')
    list_filter = ('is_hidden',)
    actions = ['hide_comments', 'show_comments']

    def hide_comments(self, request, queryset):
        queryset.update(is_hidden=True)
        self.message_user(request, "Selected comments have been hidden.")

    def show_comments(self, request, queryset):
        queryset.update(is_hidden=False)
        self.message_user(request, "Selected comments are now visible.")