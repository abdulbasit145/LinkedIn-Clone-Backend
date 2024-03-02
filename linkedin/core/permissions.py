from rest_framework import permissions

from core.constants import ADMIN, RECRUITER


class IsUser(permissions.BasePermission):
    """Custom Permission to allow himself to delete."""

    def has_permission(self, request, view):
        """If the user is owner"""
        return view.kwargs.get('pk') == request.user.pk


class IsPostOwner(permissions.BasePermission):
    """Custom permission to allow only post owners to delete their own posts. """

    def has_object_permission(self, request, view, obj):
        """Allow post owners to delete their own posts."""
        return obj.post_owner == request.user.user_profile


class IsApplicant(permissions.BasePermission):
    """Custom permission to allow only applications] owners to delete their own applicantions. """

    def has_object_permission(self, request, view, obj):
        """Allow applicantions owners to delete their own applications."""
        return obj.applicant == request.user.user_profile


class IsAdminUser(permissions.BasePermission):
    """Custom permission to allow only users with 'user_type=admin' to delete any post."""

    def has_permission(self, request, view):
        """Allow admin users to delete any post."""
        return request.user.user_type == ADMIN


class IsAdminUserOrIsPostOwner(permissions.BasePermission):
    """Custom permission to allow admin to delete any post, and post owners to delete their own posts."""

    def has_permission(self, request, view):
        """Allow admin users to delete any post."""
        if request.user.user_type == ADMIN:
            return True

        return True

    def has_object_permission(self, request, view, obj):
        """Allow post owners to delete their own posts."""
        if request.user.user_type == ADMIN:
            return True

        return obj.post_owner == request.user.user_profile


class IsRecruiter(permissions.BasePermission):
    """Custom permission to allow recruiter to post for job."""

    def has_permission(self, request, view):
        """Allow only recruiter to post for job."""
        return request.user.user_type == RECRUITER


class IsJobPostOwnerOrAdmin(permissions.BasePermission):
    """Custom permission to allow the owner of a job post or an admin to delete it."""

    def has_object_permission(self, request, view, obj):
        """Check if the user is an admin and user is the owner of the job post"""
        if request.user.user_type == ADMIN:
            return True

        return obj.recruiter.user == request.user


class IsApplicantOrAdmin(permissions.BasePermission):
    """Custom Permission to only allow admin and post owner to modify."""

    def has_object_permission(self, request, view, obj):
        """Custom Permission to only allow admin and post owner to modify."""
        if request.user.user_type == ADMIN:
            return True

        return obj.applicant.user == request.user
