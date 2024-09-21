from django.urls import path
from .views import *


urlpatterns = [
    path('posts/', PostListView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('testing/', testing.as_view()),
    path('update/<uuid:pk>/', PostActionsView.as_view()),
    path('<uuid:pk>/comments/', PostCommentListView.as_view()),
    path('comments/', CommentListCreateView.as_view()),
    path('topics/', TrendingTopicsView.as_view(),)
]