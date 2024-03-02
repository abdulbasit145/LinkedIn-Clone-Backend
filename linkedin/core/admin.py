from django.contrib import admin

from .models import CustomUser, UserProfile, Follow, Education, Experience, Certification, Course


admin.site.site_header = 'LinkedIn Clone'


class CustomUserAdmin(admin.ModelAdmin):
    """Addresses admin for Customuser Model."""

    list_display = [
        'id', 'first_name', 'last_name', 'username', 'email', 'user_type',
        'date_joined', 'is_active', 'is_staff', 'created_at', 'updated_at'
    ]
    search_fields = ['username', 'email']
    ordering = ['date_joined']
    list_filter = ['is_superuser']


class UserProfileAdmin(admin.ModelAdmin):
    """Addresses admin for UserProfile Model."""

    list_display = ['id', 'user', 'industry', 'website', 'phone_number', 'birth_date', 'location']
    search_fields = ['user', 'location']
    ordering = ['-created_at']
    list_filter = ['age']


class FollowAdmin(admin.ModelAdmin):
    """Admin for Follow model."""

    list_display = ['id', 'follower', 'following']


class EducationAdmin(admin.ModelAdmin):
    """Addresses admin for Customuser Model."""

    list_display = [
        'id', 'person', 'school', 'degree', 'field_of_study', 'start_date',
        'end_date', 'grade', 'description', 'skills', 'media'
    ]
    ordering = ['-created_at']


class ExperienceAdmin(admin.ModelAdmin):
    """Admin for Experience Model."""

    list_display = [
        'id', 'person', 'title', 'employment_type', 'company_name', 'location',
        'location_type', 'start_date', 'description', 'skills', 'media'
    ]
    ordering = ['-created_at']
    list_filter = ['employment_type', 'location_type']


class CertificationAdmin(admin.ModelAdmin):
    """Admin for Certification Model."""

    list_display = [
        'id', 'person', 'name', 'issuing_organization', 'issue_date',
        'expiration_date', 'credential_id', 'credential_url'
    ]
    ordering = ['-created_at']
    list_filter = ['issue_date']


class CourseAdmin(admin.ModelAdmin):
    """Admin for Course Model."""

    list_display = ['id', 'person', 'course_name', 'course_code', 'associated_with']
    ordering = ['-created_at']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Course, CourseAdmin)
