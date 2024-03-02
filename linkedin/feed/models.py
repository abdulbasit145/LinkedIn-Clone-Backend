from django.db import models
from django.utils import timezone

from core.models import UserProfile
from core.models import TimeStampMixin
from core.constants import LIKE, CELEBRATE, SUPPORT, LOVE, INSIGHTFUL, FUNNY


class Post(TimeStampMixin):
    """User Post."""

    post_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    parent_post = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    text_body = models.TextField(max_length=500)
    media = models.ImageField(upload_to='Posts/Media/', blank=True, null=True)
    edited = models.BooleanField(default=False, blank=True, null=True)
    reacted_by = models.ManyToManyField(UserProfile, through='PostReaction', related_name='reacted_posts')
    commented_by = models.ManyToManyField(UserProfile, through='Comment', related_name='commented_posts')

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['-created_at']

    def __str__(self):
        """String representation of the object."""
        return f"{self.post_owner.user.username} --> Post{self.id}"

    @property
    def number_of_reactions(self):
        """Number of reactions on post."""
        if self.reacted_by.count() == 1:
            return f"{self.reacted_by.count()} reaction"

        return f"{self.reacted_by.count()} reactions"

    @property
    def number_of_comments(self):
        """Number of comments on a post"""
        comments = Comment.objects.filter(post=self).count()
        if comments == 0:
            return ""
        elif comments == 1:
            return f"{comments} comment"
        return f"{comments} comments"

    @property
    def time_difference(self):
        """How long the post was uploaded."""
        time_difference = timezone.now() - self.created_at
        total_seconds = time_difference.seconds

        if time_difference.days:
            return f"{time_difference.days} day{'s' if time_difference.days > 1 else ''} ago"

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours >= 1:
            return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
        elif minutes >= 1:
            return f"{int(minutes)} minute{'s' if minutes > 1 else ''} ago"
        else:
            return f"{int(seconds)} second{'s' if seconds > 1 else ''} ago"


class ReactionType(TimeStampMixin):
    """Reaction Types on a post."""

    REACTION_TYPE_CHOICES = [
        (LIKE, "Like"),
        (CELEBRATE, "Celebrate"),
        (SUPPORT, "Support"),
        (LOVE, "Love"),
        (FUNNY, "Funny"),
        (INSIGHTFUL, "Insightful"),
    ]

    type = models.CharField(max_length=12, choices=REACTION_TYPE_CHOICES, default=None)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Reaction Type'
        verbose_name_plural = 'Reaction Types'

    def __str__(self):
        """String representation of the object."""
        return f"{self.type}"


class PostReaction(TimeStampMixin):
    """Reactions on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_reactions')
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)

    def __str__(self):
        """String representation of the object."""
        return f"{self.reaction_by.user.username} --> {self.reaction_type} --> {self.post}"


class Comment(TimeStampMixin):
    """Comments on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    reacted_by = models.ManyToManyField(UserProfile, through='CommentReaction', related_name="reacted_comments")
    replied_by = models.ManyToManyField(UserProfile, through='CommentReply', related_name="replied_comments")

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        """String representation of the object."""
        return f"Comment by --> {self.comment_owner.user.username}"

    @property
    def time_difference(self):
        """How long the post was uploaded."""
        time_difference = timezone.now() - self.created_at
        total_seconds = time_difference.seconds

        if time_difference.days:
            return f"{time_difference.days} day{'s' if time_difference.days > 1 else ''} ago"

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours >= 1:
            return f"{int(hours)} hour{'s' if hours > 1 else ''} ago"
        elif minutes >= 1:
            return f"{int(minutes)} minute{'s' if minutes > 1 else ''} ago"
        else:
            return f"{int(seconds)} second{'s' if seconds > 1 else ''} ago"


class CommentReaction(TimeStampMixin):
    """Reactions on user comment."""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reaction_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Comment Reaction'
        verbose_name_plural = 'Comment Reactions'
        unique_together = (('comment', 'reaction_owner'))


class CommentReply(TimeStampMixin):
    """Reply to a user comment"""

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    media = models.ImageField(upload_to='Comments/Media/', blank=True, null=True)
    reacted_by = models.ManyToManyField(UserProfile, through='ReplyReaction', related_name="reacted_replies")

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Comment Reply'
        verbose_name_plural = 'Comment Replies'


class ReplyReaction(TimeStampMixin):
    """Reply reaction to a comment."""

    comment_reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE)
    reaction_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reaction_type = models.ForeignKey(ReactionType, on_delete=models.CASCADE)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Reply Reaction'
        verbose_name_plural = 'Reply Reactions'
        unique_together = (('comment_reply', 'reaction_owner'))


class HashTag(TimeStampMixin):
    """Hashtags on posts."""

    topic = models.CharField(max_length=100)
    associated_posts = models.ManyToManyField(Post, related_name='hashtags')
    followed_by = models.ManyToManyField(UserProfile, related_name='followed_hashtags')

    class Meta:
        """Contains Meta option, used to change behavior of fields."""

        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'


class Notification(TimeStampMixin):
    """To implements Notifications when post is created."""

    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_notifications')

    def __str__(self):
        """String representation of the object."""
        return f"Notification for {self.recipient.user.username}"
