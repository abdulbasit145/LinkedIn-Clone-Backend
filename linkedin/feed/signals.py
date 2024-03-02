from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Notification


@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    """Create notification for followers."""
    if created:
        post_owner = instance.post_owner
        followers = post_owner.followers.all()
        for follower in followers:
            notification = Notification(
                recipient=follower.follower,
                message=f"{post_owner.user.username} created a new post.",
                post=instance
            )
            notification.save()
