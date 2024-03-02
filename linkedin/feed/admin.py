from django.contrib import admin

from .models import (
    Post, ReactionType, PostReaction, Comment, Notification,
    CommentReaction, CommentReply, ReplyReaction, HashTag
)


class PostAdmin(admin.ModelAdmin):
    """Addresses admin for Post Model."""

    list_display = ('id', 'post_owner', 'parent_post', 'text_body', 'edited')


class ReactionTypeAdmin(admin.ModelAdmin):
    """Addresses admin for Reaction type model."""

    list_display = ('id', 'type', 'created_at')


class PostReactionAdmin(admin.ModelAdmin):
    """Addresses admin for Post reactions Model."""

    list_display = ('id', 'post', 'reaction_by', 'reaction_type', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    """Addresses admin for Comments Model."""

    list_display = ('id', 'post', 'comment_owner', 'text', 'created_at')


class CommentReactionAdmin(admin.ModelAdmin):
    """Addresses admin for Comments reactions Model."""

    list_display = ('id', 'comment', 'reaction_owner', 'reaction_type', 'created_at')


class CommentReplyAdmin(admin.ModelAdmin):
    """Addresses admin for Comments reply Model."""

    list_display = ('id', 'comment', 'reply_owner', 'text', 'created_at')


class ReplyReactionAdmin(admin.ModelAdmin):
    """Addresses admin for reply reaction Model."""

    list_display = ('id', 'comment_reply', 'reaction_owner', 'reaction_type', 'created_at')


class HashTagAdmin(admin.ModelAdmin):
    """Addresses admin for hashtag Model."""

    list_display = ('id', 'topic', 'created_at')


class NotificationAdmin(admin.ModelAdmin):
    """Addresses admin for Notification Model."""

    list_display = ('id', 'recipient', 'message', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(ReactionType, ReactionTypeAdmin)
admin.site.register(PostReaction, PostReactionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)
admin.site.register(ReplyReaction, ReplyReactionAdmin)
admin.site.register(CommentReaction, CommentReactionAdmin)
admin.site.register(HashTag, HashTagAdmin)
admin.site.register(Notification, NotificationAdmin)
