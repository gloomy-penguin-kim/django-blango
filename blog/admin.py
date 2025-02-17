from django.contrib import admin
from blog.models import Tag, Post, Comment, AuthorProfile


admin.site.register(Tag)

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'author', 'published_at')


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_object_str', 'content_type', 'creator')

    def content_object_str(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return '-'
    
admin.site.register(Comment, CommentAdmin)

admin.site.register(AuthorProfile)