from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from .models import UserProfile, Follow, CustomUser, Experience, Education, Certification, Course

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for user of the app."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'user_type']


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer to register new user to the app."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmed_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = User
        fields = ('username', 'password', 'confirmed_password', 'email', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, attrs):
        """To validate the password.

        :param attrs: Dictionary containing validated data.
        :returns: Validation error if password doesn't match else validated data.
        """
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """To create new user data, in the database.

        :param attrs: Dictionary containing validated data.
        :returns: Newly created user object.
        """
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer class to change user password."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmed_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = User
        fields = ('old_password', 'password', 'confirmed_password')

    def validate(self, attrs):
        """To validate the new password.

        :param attrs: Dictionary containing validated data.
        :returns: Validation error if password doesn't match else validated data.
        """
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        """To validate the old password.

        :param value: Old password provided for validation.
        :returns: Validation error if old password is not correct else validated old password is returned.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        """To update user data, in the database.

        :param instance: user instance to be updated.
        :param validated_data: Dictionary containing validated data.
        :returns: Updated user object.
        """
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    """Serializer to update username, first_name, last_name and password."""

    email = serializers.EmailField(required=True)

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def update(self, instance, validated_data):
        """To update user data, in the database.

        :param instance: user instance to be updated.
        :param validated_data: Dictionary containing validated data.
        :returns: Updated user object.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class GetUserProfileSerializer(serializers.ModelSerializer):
    """Serializer class for the user."""

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = UserProfile
        fields = (
            'id', 'user', 'profile_pic', 'cover_pic', 'headline', 'summary',
            'location', 'industry', 'website', 'phone_number', 'birth_date',
            'age', 'gender', 'followers_count', 'following_count'
        )

    def get_followers_count(self, obj):
        """Number of followers for this UserProfile.

        :param obj: The user profile instance.
        :returns: number of followers for provided instance.
        """
        return obj.following.count()

    def get_following_count(self, obj):
        """Number of people this UserProfile is following.

        :param obj: The user profile instance.
        :returns: number of people this instance is following.
        """
        return obj.followers.count()


class CreateUserProfileSerializer(serializers.ModelSerializer):
    """Serializer to create new profile"""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = UserProfile
        fields = (
            'profile_pic', 'cover_pic', 'headline', 'summary', 'location', 'industry', 'website', 'phone_number',
            'birth_date', 'age', 'gender'
        )


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    """Serializer to update user profile"""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = UserProfile
        fields = (
            'profile_pic', 'cover_pic', 'headline', 'summary', 'location', 'industry', 'website', 'phone_number',
            'birth_date', 'age', 'gender'
        )


class FollowSerializer(serializers.ModelSerializer):
    """Serializer class to follow a user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Follow
        fields = ['following']


class GetFollowSerializer(serializers.ModelSerializer):
    """Serializer to get follwers for a user."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Follow
        fields = '__all__'


class GetExperienceSerializer(serializers.ModelSerializer):
    """Serializer class to get follow a user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Experience
        fields = '__all__'


class CreateExperienceSerializer(serializers.ModelSerializer):
    """Serializer class to add experience to user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Experience
        fields = (
            'person', 'title', 'employment_type', 'company_name', 'location', 'location_type', 'start_date',
            'description', 'skills', 'media'
        )


class UpdateExperienceSerializer(serializers.ModelSerializer):
    """Serializer class to update experience of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Experience
        fields = (
            'title', 'employment_type', 'company_name', 'location', 'location_type', 'start_date',
            'description', 'skills', 'media'
        )


class GetEducationSerializer(serializers.ModelSerializer):
    """Serializer class to display education of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Education
        fields = '__all__'


class CreateEducationSerializer(serializers.ModelSerializer):
    """Serializer class to add education to user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Education
        fields = (
            'person', 'school', 'degree', 'field_of_study', 'start_date', 'end_date', 'grade', 'description',
            'skills', 'media'
        )


class UpdateEducationSerializer(serializers.ModelSerializer):
    """Serializer class to update education of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Education
        fields = (
            'school', 'degree', 'field_of_study', 'start_date', 'end_date', 'grade',
            'description', 'skills', 'media'
        )


class GetCertificationSerializer(serializers.ModelSerializer):
    """Serializer class to display certifications of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Certification
        fields = '__all__'


class CreateCertificationSerializer(serializers.ModelSerializer):
    """Serializer class to add certification to user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Certification
        fields = (
            'person', 'name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_id',
            'credential_url', 'skills'
        )


class UpdateCertificationSerializer(serializers.ModelSerializer):
    """Serializer class to update certifications of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Certification
        fields = (
            'name', 'issuing_organization', 'issue_date', 'expiration_date', 'credential_id',
            'credential_url', 'skills'
        )


class GetCourseSerializer(serializers.ModelSerializer):
    """Serializer class to display courses of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Course
        fields = '__all__'


class CreateCourseSerializer(serializers.ModelSerializer):
    """Serializer class to add courses to user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Course
        fields = ('person', 'course_name', 'course_code', 'associated_with')


class UpdateCoursesSerializer(serializers.ModelSerializer):
    """Serializer class to update courses of user profile."""

    class Meta:
        """Contains meta option, used to change behavior of fields."""

        model = Course
        fields = ('course_name', 'course_code', 'associated_with')
