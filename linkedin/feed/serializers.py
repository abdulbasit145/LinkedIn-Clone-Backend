from rest_framework import serializers

from .models import (
    Post, ReactionType, PostReaction, Comment, CommentReaction, CommentReply, ReplyReaction, Notification
)


class CreatePostSerializer(serializers.ModelSerializer):
    """Serializer class to create Post for logged in user."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Post
        fields = ('parent_post', 'text_body', 'media')


class UpdatePostSerializer(serializers.ModelSerializer):
    """Serializer class to update education of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Post
        fields = ('parent_post', 'text_body', 'media',)


class GetPostSerializer(serializers.ModelSerializer):
    """Serializer class to display certifications of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Post
        fields = (
            'id', 'post_owner', 'parent_post', 'text_body', 'media', 'edited', 'reacted_by', 'commented_by',
            'number_of_reactions', 'number_of_comments', 'time_difference',
        )


class ReactionTypeSerializer(serializers.ModelSerializer):
    """Serializer for Reaction types."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = ReactionType
        fields = '__all__'


class CreateReactionTypeSerializer(serializers.ModelSerializer):
    """Serializer to create new reaction type."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = ReactionType
        fields = ('type',)


class PostReactionSerializer(serializers.ModelSerializer):
    """Serializer to react on post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = PostReaction
        fields = ('post', 'reaction_type')


class GetPostReactionSerializer(serializers.ModelSerializer):
    """Serializer to get reactions on post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = PostReaction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments on post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Comment
        fields = ('post', 'text',)


class GetCommentSerializer(serializers.ModelSerializer):
    """Serializer to get comments on post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Comment
        fields = ('id', 'post', 'comment_owner', 'text', 'reacted_by', 'replied_by', 'time_difference',)


class CommenReactionSerializer(serializers.ModelSerializer):
    """Serializer to react on comment."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = CommentReaction
        fields = ('comment', 'reaction_type')


class GetCommentReactionSerializer(serializers.ModelSerializer):
    """Serializer to get reactions on comments."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = CommentReaction
        fields = '__all__'


class CommentReplySerializer(serializers.ModelSerializer):
    """Serializer for replies on comment."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = CommentReply
        fields = ('comment', 'text', 'media')


class UpdateCommentReplySerializer(serializers.ModelSerializer):
    """Serializer for replies on comment."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = CommentReply
        fields = ('text', 'media')


class GetCommentReplySerializer(serializers.ModelSerializer):
    """Serializer for replies on comment."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = CommentReply
        fields = '__all__'


class ReplyReactionSerializer(serializers.ModelSerializer):
    """Serializer for reaction on comment reply."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = ReplyReaction
        fields = ('comment_reply', 'reaction_type')


class GetReplyReactionSerializer(serializers.ModelSerializer):
    """Serializer for reaction on comment reply."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = ReplyReaction
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer class for Notification."""

    class Meta:
        """Contains Meta option, used to change behavior of fields."""
        model = Notification
        fields = '__all__'
