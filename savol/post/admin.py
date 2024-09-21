from django.contrib import admin
from .models import Post, PostLike, PostComment, CommentLike, Topic


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_time')
    search_fields = ('id', 'author__username', 'caption')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-created_time')
        return queryset


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_time')
    search_fields = ('id', 'author__username', 'comment')


class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_time')
    search_fields = ('id', 'author__username')


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_time')
    search_fields = ('id', 'author__username')


admin.site.register(Topic)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, CommentAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
