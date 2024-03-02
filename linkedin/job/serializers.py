from rest_framework import serializers

from .models import JobPost, JobApplication


class JobPostSerializer(serializers.ModelSerializer):
    """Serializer to create Job Post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = JobPost
        fields = ('title', 'description',)


class GetJobPostSerializer(serializers.ModelSerializer):
    """Serializer to create Job Post."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = JobPost
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer to create Application for Job."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = JobApplication
        fields = ('job', 'cover_letter', 'resume')


class UpdateJobApplicationSerializer(serializers.ModelSerializer):
    """Serializer to update Application for Job."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = JobApplication
        fields = ('cover_letter', 'resume')


class GetJobApplicationSerializer(serializers.ModelSerializer):
    """Serializer to get Application for Job."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = JobApplication
        fields = '__all__'
