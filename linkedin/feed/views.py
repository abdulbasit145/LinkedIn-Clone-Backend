from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from core.permissions import IsPostOwner, IsAdminUser, IsAdminUserOrIsPostOwner
from .models import (
    Post, ReactionType, PostReaction, Comment, CommentReaction, CommentReply, ReplyReaction, Notification
)
from .serializers import (
    GetPostSerializer, UpdatePostSerializer, CreatePostSerializer, ReactionTypeSerializer,
    CreateReactionTypeSerializer, PostReactionSerializer, GetPostReactionSerializer, CommentSerializer,
    GetCommentSerializer, GetCommentReactionSerializer, CommenReactionSerializer, CommentReplySerializer,
    GetCommentReplySerializer, UpdateCommentReplySerializer, ReplyReactionSerializer, GetReplyReactionSerializer,
    NotificationSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostOwner]

    def get_serializer_class(self):
        """Serializer class on specific action method."""
        if self.action == 'create':
            return CreatePostSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdatePostSerializer
        return GetPostSerializer

    def get_permissions(self):
        """Allow Admin to delete any post and non admin to delete their own posts."""
        if self.action == 'destroy':
            return [IsAdminUserOrIsPostOwner()]
        elif self.action == 'retrieve':
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create Post for logged in User.

        :param serializer:
        """
        serializer.save(post_owner=self.request.user.user_profile, edited=False)

    def perform_update(self, serializer):
        """Update Post for logged in User.

        :param serializer:
        """
        serializer.save(post_owner=self.request.user.user_profile, edited=True)


class ReactionTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions for reaction types.
    """

    queryset = ReactionType.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ReactionTypeSerializer

    def create(self, request, *args, **kwargs):
        """To create reaction type.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = CreateReactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """To delete reaction type.

        :param request:
        :param *args:
        :param **kwargs:
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """To show error on updation.

        :param request:
        :param *args:
        :param **kwargs:
        """
        return Response("Updation of reaction types is not allowed")

    def partial_update(self, request, *args, **kwargs):
        """ To show error on updation.

        :param request:
        :param *args:
        :param **kwargs:
        """
        return Response("partial Updation of reaction types is not allowed")


class CreatePostReactionView(generics.CreateAPIView):
    """To react on post."""

    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """To create reaction for post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_id = request.data.get('post')
        user_profile = request.user.user_profile

        existing_reaction = PostReaction.objects.filter(post_id=post_id, reaction_by=user_profile).first()

        if existing_reaction:
            existing_reaction.reaction_type = serializer.validated_data['reaction_type']
            existing_reaction.save()
            response_message = "Reaction updated."
        else:
            serializer.save(reaction_by=user_profile)
            response_message = "Reaction created."

        post = Post.objects.get(pk=post_id)
        post.reacted_by.add(user_profile)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": response_message}, status=status.HTTP_201_CREATED, headers=headers)


class RemovePostReactionView(generics.DestroyAPIView):
    """To remove reactions on posts."""

    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PostReaction.objects.all()

    def perform_destroy(self, instance):
        """To delete reaction post.

        :param instance:
        """
        reaction = self.get_object()
        user_profile = self.request.user.user_profile

        if reaction.reaction_by == user_profile:
            post = instance.post
            post.reacted_by.remove(user_profile)
            instance.delete()
            response_message = "Reaction removed successfully"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            response_message = "You can't remove the reaction of another user"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def destroy(self, request, *args, **kwargs):
        """To delete reaction for post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_destroy(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class ListPostReactionsView(generics.ListAPIView):
    """Yo list reactions on post."""
    serializer_class = GetPostReactionSerializer

    def get_queryset(self):
        """return reactions on specific post."""
        post_id = self.kwargs['post_id']
        return PostReaction.objects.filter(post=post_id)


class CreateCommentView(generics.CreateAPIView):
    """To create comment for a post."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """To create comment for post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_id = request.data.get('post')
        user_profile = request.user.user_profile

        serializer.save(comment_owner=user_profile)
        response_message = "Comment created."

        post = Post.objects.get(pk=post_id)
        post.commented_by.add(user_profile)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": response_message}, status=status.HTTP_201_CREATED, headers=headers)


class UpdateCommentView(generics.UpdateAPIView):
    """To update comment on a post."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """To update comment for post.

        :param serializer:
        """
        comment = self.get_object()

        if comment.comment_owner == self.request.user.user_profile:
            comment.text = self.request.data.get('text')
            comment.save()
            response_message = "Comment updated"
            status_code = status.HTTP_200_OK
        else:
            response_message = "You can't update another user's comment"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def update(self, request, *args, **kwargs):
        """To update comment for post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_update(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class RemoveCommentView(generics.DestroyAPIView):
    """To remove comment on a post."""

    serializer_class = PostReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_destroy(self, instance):
        """To delete comment for post.

        :param instance:
        """
        comment = self.get_object()

        if comment.comment_owner == self.request.user.user_profile:
            comment.delete()
            response_message = "Comment removed successfully"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            response_message = "You can't remove the comment of another user"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def destroy(self, request, *args, **kwargs):
        """To delete comment for post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_destroy(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class ListCommentsForPostView(generics.ListAPIView):
    """To List comments for post."""

    serializer_class = GetCommentSerializer

    def get_queryset(self):
        """return comments for specific post."""
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post=post_id)


class CreateCommentReactionView(generics.CreateAPIView):
    """To react on comment."""

    serializer_class = CommenReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """To create comment reaction on post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_id = request.data.get('comment')
        user_profile = request.user.user_profile

        existing_reaction = CommentReaction.objects.filter(comment=comment_id, reaction_owner=user_profile).first()

        if existing_reaction:
            existing_reaction.reaction_type = serializer.validated_data['reaction_type']
            existing_reaction.save()
            response_message = "Comment Reaction updated."
        else:
            serializer.save(reaction_owner=user_profile)
            response_message = "Comment Reaction created."

        post = Comment.objects.get(pk=comment_id)
        post.reacted_by.add(user_profile)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": response_message}, status=status.HTTP_201_CREATED, headers=headers)


class RemoveCommentReactionView(generics.DestroyAPIView):
    """To remove comment reaction."""

    serializer_class = CommenReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CommentReaction.objects.all()

    def perform_destroy(self, instance):
        """To delete comment reaction on post.

        :param instance
        """
        reaction = self.get_object()
        user_profile = self.request.user.user_profile

        if reaction.reaction_owner == user_profile:
            comment = instance.comment
            comment.reacted_by.remove(user_profile)
            instance.delete()
            response_message = "Comment Reaction removed successfully"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            response_message = "You can't remove the reaction of another user comment"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def destroy(self, request, *args, **kwargs):
        """To delete comment reaction on post.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_destroy(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class ListCommentReactionView(generics.ListAPIView):
    """List comment reaction on a comment."""

    serializer_class = GetCommentReactionSerializer

    def get_queryset(self):
        """return reactions for a specific comment."""
        comment_id = self.kwargs['comment_id']
        return CommentReaction.objects.filter(comment=comment_id)


class CreateCommentReplyView(generics.CreateAPIView):
    """To create comment reply for a comment."""

    serializer_class = CommentReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """To create comment reply on comment.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_id = request.data.get('comment')
        user_profile = request.user.user_profile

        serializer.save(reply_owner=user_profile)
        response_message = "Comment Replied."

        comment = Comment.objects.get(pk=comment_id)
        print(comment)
        comment.replied_by.add(user_profile)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": response_message}, status=status.HTTP_201_CREATED, headers=headers)


class UpdateCommentReplyView(generics.UpdateAPIView):
    """Update comment reply on a comment."""

    queryset = CommentReply.objects.all()
    serializer_class = UpdateCommentReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """To updare comment reply on comment.

        :param serializer:
        """
        comment = self.get_object()

        if comment.reply_owner == self.request.user.user_profile:
            comment.text = self.request.data.get('text')
            comment.save()
            response_message = "Comment reply updated"
            status_code = status.HTTP_200_OK
        else:
            response_message = "You can't update another user's comment"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def update(self, request, *args, **kwargs):
        """To update comment reply on comment.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_update(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class RemoveCommentReplyView(generics.DestroyAPIView):
    """To delete comment reply on comment."""

    serializer_class = CommentReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CommentReply.objects.all()

    def perform_destroy(self, instance):
        """To delete comment reply on comment.

        :param instance:
        """
        comment = self.get_object()

        if comment.reply_owner == self.request.user.user_profile:
            comment.delete()
            response_message = "Comment reply removed successfully"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            response_message = "You can't remove the comment reply of another user"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def destroy(self, request, *args, **kwargs):
        """To delete comment reply on comment.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_destroy(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class ListCommentRepliesView(generics.ListAPIView):
    """To list comment replies on comment."""

    serializer_class = GetCommentReplySerializer

    def get_queryset(self):
        """return replies for specific comment."""
        comment_id = self.kwargs['comment_id']
        return CommentReply.objects.filter(comment=comment_id)


class CreateReplyReactionView(generics.CreateAPIView):
    """To react on replies on a comment."""

    serializer_class = ReplyReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """To create reaction on comment replies.

        :param request:
        :param *args:
        :param **kwargs:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_id = request.data.get('comment_reply')
        user_profile = request.user.user_profile

        existing_reaction = ReplyReaction.objects.filter(comment_reply=comment_id, reaction_owner=user_profile).first()

        if existing_reaction:
            existing_reaction.reaction_type = serializer.validated_data['reaction_type']
            existing_reaction.save()
            response_message = "Comment Reply Reaction updated."
        else:
            serializer.save(reaction_owner=user_profile)
            response_message = "Comment Reaction created."

        comment = CommentReply.objects.get(pk=comment_id)
        comment.reacted_by.add(user_profile)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": response_message}, status=status.HTTP_201_CREATED, headers=headers)


class RemoveReplyreactionview(generics.DestroyAPIView):
    """To remove reaction comment replies."""

    serializer_class = ReplyReactionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ReplyReaction.objects.all()

    def perform_destroy(self, instance):
        """To delete reaction on comment replies.

        :param instance:
        """
        reaction = self.get_object()
        user_profile = self.request.user.user_profile

        if reaction.reaction_owner == user_profile:
            comment = instance.comment_reply
            comment.reacted_by.remove(user_profile)
            instance.delete()
            response_message = "Comment reply Reaction removed successfully"
            status_code = status.HTTP_204_NO_CONTENT
        else:
            response_message = "You can't remove the reaction of another user comment"
            status_code = status.HTTP_403_FORBIDDEN

        return response_message, status_code

    def destroy(self, request, *args, **kwargs):
        """To delete reaction on comment replies.

        :param request:
        :param *args:
        :param **kwargs:
        """
        response_message, status_code = self.perform_destroy(self.get_object())
        return Response({"detail": response_message}, status=status_code)


class ListReplyReactionView(generics.ListAPIView):
    """List reaction on a specic reply."""
    serializer_class = GetReplyReactionSerializer

    def get_queryset(self):
        """return reply reaction for specic comment reply."""
        comment_id = self.kwargs['reply_comment_id']
        return ReplyReaction.objects.filter(comment_reply=comment_id)


class NotificationList(generics.ListAPIView):
    """To list notifications."""

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
