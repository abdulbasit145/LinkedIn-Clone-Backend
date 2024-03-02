from django.contrib import admin

from .models import JobPost, Tag, JobApplication


class JobPostAdmin(admin.ModelAdmin):
    """Addresses admin for the JobPost."""

    list_display = ('id', 'title', 'description', 'recruiter')


class TagAdmin(admin.ModelAdmin):
    """Addresses admin for the Tags."""

    list_display = ('id', 'name')


class JobApplicationAdmin(admin.ModelAdmin):
    """Addresses admin for the Job Application."""

    list_display = ('id', 'job', 'applicant', 'cover_letter', 'resume', 'applied_at')
    search_fields = ['job']


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
