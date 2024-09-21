from .serializers import *
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from django.db.models import Count
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from shared.custom_pagination import CustomPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class testing(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        return Response({"status":"ok"})
    

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )
    pagination_class = CustomPagination

    def get_queryset(self):
        return Post.objects.all()
    

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)


class PostActionsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer()
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data = request.data)
        serializer.is_valid(raise_exceptions=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_200_OK)
    

class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny, )
    pagination_class = CustomPagination
    
    def get_queryset(self):
        post_id = self.kwargs['pk']
        queryset = PostComment.objects.filter(post__id=post_id)
        return queryset
    

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostComment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TrendingTopicsView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        one_week_ago = timezone.now() - timedelta(weeks=1)

        top_topics = Topic.objects.filter(
            posts__created_time__gte=one_week_ago
        ).annotate(
            num_posts=Count('posts')
        ).order_by('-num_posts')[:15]

        if len(top_topics) < 5:
            additional_topics = Topic.objects.exclude(
                id__in=top_topics.values_list('id', flat=True)
            ).annotate(
                num_posts=Count('posts')
            ).order_by('-num_posts')[:5 - len(top_topics)]
            top_topics = list(top_topics) + list(additional_topics)

        serializer = TopicSerializer(top_topics, many=True)

        return Response(serializer.data)
