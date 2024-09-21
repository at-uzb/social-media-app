from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Post, PostLike, PostComment, CommentLike, Topic


class TopicSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    num_posts = serializers.SerializerMethodField('count_posts')

    class Meta:
        model = Topic
        fields = ['id', 'name', 'image', 'author', 'num_posts']

    def get_author(self, object):
        return object.created_by.username
    
    def count_posts(self, object):
        return object.posts.count()

class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    author = UserSerializer(read_only = True)
    post_likes = serializers.SerializerMethodField('get_post_likes_count')
    post_comment_count = serializers.SerializerMethodField('get_post_comment_count')
    liked = serializers.SerializerMethodField("get_liked")
    image = serializers.SerializerMethodField('get_image_urls')
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(), required=False)

    class Meta:
        model = Post
        fields = [
            'id', 
            'author',
            'image1',
            'image2',
            'image3',
            'image', 
            'caption', 
            'created_time', 
            'post_likes', 
            'post_comment_count',
            'liked',
            'topic'
        ]
        
    def get_post_likes_count(self, obj):
        return obj.likes.count()
    
    def get_post_comment_count(self, obj):
        return obj.comments.count()
    
    def get_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                PostLike.objects.get(post=obj, author = request.user)
                return True
            except PostLike.DoesNotExist:
                return False
        return False
    
    def get_image_urls(self, obj):
        images = [obj.image1, obj.image2, obj.image3]
        return [image.url for image in images if image]


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField('get_replies')
    liked = serializers.SerializerMethodField('get_liked')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = PostComment
        fields = [
            "id", 
            'author', 
            'post',
            'comment', 
            'parent', 
            'created_time', 
            'replies', 
            'likes_count',
            'liked'
        ]
    
    def get_replies(self, object):
        if object.child.exists():
            serializers = self.__class__(object.child.all(), many=True, context=self.context)
            return serializers.data
        else:
            return None
        
    def get_liked(self, object):
        user = self.context.get('request').user
        if user.is_authenticated:
            return object.likes.filter(author=user).exists()
        else:
            return False
    def get_likes_count(self, object):
        return object.likes.count()


class CommentLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'author', 'comment_id')


class PostLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'author', 'post_id']