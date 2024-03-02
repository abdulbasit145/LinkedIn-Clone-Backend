from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.permissions import IsRecruiter, IsJobPostOwnerOrAdmin, IsApplicant, IsApplicantOrAdmin
from .models import JobPost, JobApplication
from .serializers import (
    GetJobPostSerializer, JobPostSerializer, JobApplicationSerializer,
    GetJobApplicationSerializer, UpdateJobApplicationSerializer
)


class JobPostViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = JobPost.objects.all()

    def get_serializer_class(self):
        """Serializer class on specific action method."""
        if self.action in ['create', 'update', 'partial_update']:
            return JobPostSerializer
        return GetJobPostSerializer

    def get_permissions(self):
        "Allow admin to delete any job and recruiter only to post job."
        if self.action == 'destroy':
            return [IsJobPostOwnerOrAdmin(), IsAuthenticatedOrReadOnly()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsRecruiter(), IsAuthenticatedOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        """Create Job Post by recruiter.

        :param serializer:
        """
        serializer.save(recruiter=self.request.user.user_profile)

    def perform_update(self, serializer):
        """Update Job Post by recruiter.

        :param serializer:
        """
        serializer.save(recruiter=self.request.user.user_profile)


class JobApplicationViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    queryset = JobApplication.objects.all()

    def get_serializer_class(self):
        """Serializer class on specific action method."""
        if self.action == 'create':
            return JobApplicationSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateJobApplicationSerializer
        return GetJobApplicationSerializer

    def get_permissions(self):
        "Allow job application owner to delete  job application."
        if self.action == 'destroy':
            return [IsApplicantOrAdmin(), IsAuthenticatedOrReadOnly()]
        elif self.action in ['update', 'partial_update']:
            return [IsApplicant(), IsAuthenticatedOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        """Create Job Application.

        :param serializer:
        """
        serializer.save(applicant=self.request.user.user_profile)

    def perform_update(self, serializer):
        """Update Job Application.

        :param serializer:
        """
        serializer.save(applicant=self.request.user.user_profile)
