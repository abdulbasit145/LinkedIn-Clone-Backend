from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PostViewSet, ReactionTypeViewSet, CreatePostReactionView, RemovePostReactionView,
    ListPostReactionsView, CreateCommentView, UpdateCommentView, RemoveCommentView,
    ListCommentsForPostView, CreateCommentReactionView, RemoveCommentReactionView,
    ListCommentReactionView, CreateCommentReplyView, UpdateCommentReplyView,
    RemoveCommentReplyView, ListCommentRepliesView, CreateReplyReactionView,
    RemoveReplyreactionview, ListReplyReactionView, NotificationList
)

app_name = 'feed'

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'reaction-types', ReactionTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('reaction/create/', CreatePostReactionView.as_view(), name='create-update-reaction'),
    path('reaction/remove/<int:pk>/', RemovePostReactionView.as_view(), name='remove-reaction'),
    path('reaction/list/<int:post_id>/', ListPostReactionsView.as_view(), name='list-reactions-for-post'),

    path('comments/create/', CreateCommentView.as_view(), name='create-comment'),
    path('comments/update/<int:pk>/', UpdateCommentView.as_view(), name='update-comment'),
    path('comments/delete/<int:pk>/', RemoveCommentView.as_view(), name='remove-comment'),
    path('comments/list/<int:post_id>/', ListCommentsForPostView.as_view(), name='list-comments-for-post'),

    path('comments-reactions/create/', CreateCommentReactionView.as_view(), name='create-update-comment-reaction'),
    path('comments-reactions/remove/<int:pk>/', RemoveCommentReactionView.as_view(), name='remove-comment-reaction'),
    path(
        'comments-reactions/list/<int:comment_id>/', ListCommentReactionView.as_view(),
        name='list-reactions-for-comment'
    ),

    path('comment-replies/create/', CreateCommentReplyView.as_view(), name='create_comment_reply'),
    path('comment-replies/update/<int:pk>/', UpdateCommentReplyView.as_view(), name='update-reply-comment'),
    path('comment-replies/delete/<int:pk>/', RemoveCommentReplyView.as_view(), name='remove-reply-comment'),
    path(
        'comment-replies/list/<int:comment_id>/', ListCommentRepliesView.as_view(),
        name='list-comments-replies-on-comment'
    ),

    path('reply-reactions/create/', CreateReplyReactionView.as_view(), name='create-update-comment-reply-reaction'),
    path('reply-reactions/remove/<int:pk>/', RemoveReplyreactionview.as_view(), name='remove-comment-reply-reaction'),
    path(
        'reply-reactions/list/<int:reply_comment_id>/', ListReplyReactionView.as_view(),
        name='list-reply-reactions-for-comment'
    ),

    path('notifications/', NotificationList.as_view(), name='notification'),
]
