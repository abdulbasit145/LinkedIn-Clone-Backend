from django.db import models

from core.models import UserProfile, TimeStampMixin


class JobPost(TimeStampMixin):
    "Model for job posting."

    title = models.CharField(max_length=255)
    description = models.TextField()
    recruiter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posted_jobs')
    tags = models.ManyToManyField('Tag', related_name='jobs')
    applicants = models.ManyToManyField(UserProfile, through='JobApplication', related_name='applied_jobs')

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Job Post'
        verbose_name_plural = 'Job Posts'
        ordering = ['-created_at']

    def __str__(self):
        """String represntation of the object instance."""
        return self.title


class Tag(TimeStampMixin):
    """Model for job tags."""

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """String represntation of the object instance."""
        return self.name


class JobApplication(TimeStampMixin):
    """Model for Job Application."""

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='JobApplications/Resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        ordering = ['-applied_at']

    def __str__(self):
        """String represntation of the object instance."""
        return f"{self.applicant.user.username} applied for {self.job.title}"
