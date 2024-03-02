from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied

from .permissions import IsUser
from .models import UserProfile, Follow, CustomUser, Experience, Education, Certification, Course
from .serializers import (
    GetUserProfileSerializer, CreateUserProfileSerializer, RegistrationSerializer, ChangePasswordSerializer,
    FollowSerializer, UpdateUserProfileSerializer, CustomUserSerializer, GetFollowSerializer, UpdateUserSerializer,
    CreateExperienceSerializer, UpdateExperienceSerializer, GetEducationSerializer, GetExperienceSerializer,
    UpdateEducationSerializer, CreateEducationSerializer, GetCertificationSerializer, CreateCourseSerializer,
    UpdateCertificationSerializer, CreateCertificationSerializer, GetCourseSerializer, UpdateCoursesSerializer,
)

User = get_user_model()


class UserListView(generics.ListAPIView):
    """To Lists users of the applications."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    """To Delete users of the applications."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsUser]


class ChangePasswordView(generics.UpdateAPIView):
    """View to Change old password."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = ChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        """To not allow PATCH method."""
        raise PermissionDenied("PATCH and other methods are not allowed.")


class UpdateUserView(generics.UpdateAPIView):
    """View to Update User Profile."""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    """To Logout user from a device."""

    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request):
        """Logs out a user by blacklisting their refresh token.

        :param request: HTTP request object
        :return: response object with status code 205 if success else 400 status code.
        """
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successfully logged out.", status=status.HTTP_205_RESET_CONTENT)

        except Exception:
            return Response("Logout failed. Please try again.", status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """To Logout user from all devices."""

    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request):
        """Logs all users by blacklisting all the refresh tokens.

        :param request: HTTP request object
        :return: response object with status code 205"""
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            _, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class UserRegistrationView(generics.CreateAPIView):
    """View to register new user."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions."""

    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Serialzer classess on specific action methods."""
        if self.action in ['create']:
            return CreateUserProfileSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserProfileSerializer
        return GetUserProfileSerializer

    def perform_create(self, serializer):
        """Override the perform_create method to set the user."""
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """ Check if the user can update profile and update profile.
        :param request:
        :param *args:
        :param **kwargs:
        :return updated profile.
        """
        instance = self.get_object()
        if instance.user == request.user:
            return super().update(request, *args, **kwargs)
        return Response("You do not have permission to update others profile.", status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        """ Check if the user can update profile and update profile.
        :param request:
        :param *args:
        :param **kwargs:
        :return: updated profile.
        """
        instance = self.get_object()
        if instance.user == request.user:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            "You do not have permission to partially update others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        """ Check if the user can delete profile and delete profile.
        :param request:
        :param *args:
        :param **kwargs:
        :return: delete profile.
        """
        instance = self.get_object()
        if instance.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response("You do not have permission to delete others profile.", status=status.HTTP_403_FORBIDDEN)


class FollowCreateView(generics.CreateAPIView):
    """To Create following relationship with a user profile."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create following relationship and response if already followed."""
        follower = self.request.user.user_profile
        following_user = serializer.validated_data.get('following')

        existing_relationship = Follow.objects.filter(follower=follower, following=following_user).first()

        if existing_relationship:
            raise PermissionDenied("You are already following this user.")
        elif follower == following_user:
            raise PermissionDenied("You can't folllow yourself.")
        else:
            serializer.save(follower=follower)


class FollowerListView(generics.ListAPIView):
    """View to list followers user profiles."""

    serializer_class = GetFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """To get current user profile."""
        user = self.request.user.user_profile
        return Follow.objects.filter(following=user)


class FollowingListView(generics.ListAPIView):
    """View to list following user profiles."""

    serializer_class = GetFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """To get current user profile."""
        user = self.request.user.user_profile
        return Follow.objects.filter(follower=user)


class UnfollowView(generics.DestroyAPIView):
    """Vire to unfollow a user profile."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, profile_id, *args, **kwargs):
        """Check if the user profile exists and then unfollow them.

            :param request:
            :param profile_id:
            :param *args:
            :param **kwargs:.
        """
        try:
            unfollowed_user_profile = UserProfile.objects.get(pk=profile_id)
        except UserProfile.DoesNotExist:
            return Response("User profile not found.", status=status.HTTP_404_NOT_FOUND)

        follow_relationship = Follow.objects.filter(
            follower=request.user.user_profile, following=unfollowed_user_profile
        ).first()
        if follow_relationship:
            follow_relationship.delete()
            return Response("You have unfollowed the user.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not following this user.", status=status.HTTP_400_BAD_REQUEST)


class ExperienceViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions."""

    queryset = Experience.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create']:
            return CreateExperienceSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateExperienceSerializer
        return GetExperienceSerializer

    def create(self, request, *args, **kwargs):
        """Check if the user can create experience and create experience.
        :param request:
        :param *args:
        :param **kwargs:
        :return: create experience.
        """
        if request.data.get('person') != str(request.user.id):
            raise PermissionDenied("You do not have permission to add Experience for another user.")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Check if the user can update experience and update experience.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update experience.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().update(request, *args, **kwargs)
        return Response(
            "You do not have permission to update Experience for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        """Check if the user can update experience and update experience.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update experience.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            "You do not have permission to partially update Experience for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        """Check if the user can delete experience and delete experience.
        :param request:
        :param *args:
        :param **kwargs:
        :return: delete experience.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response(
            "You do not have permission to delete Experience for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )


class EducationViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions."""

    queryset = Education.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Serializer on specific action methods."""
        if self.action in ['create']:
            return CreateEducationSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateEducationSerializer
        return GetEducationSerializer

    def create(self, request, *args, **kwargs):
        """Check if the user can create education and create education.
        :param request:
        :param *args:
        :param **kwargs:
        :return: create education.
        """
        if request.data.get('person') != str(request.user.id):
            raise PermissionDenied("You do not have permission to add Education for another user.")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Check if the user can update education and update education.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update education.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().update(request, *args, **kwargs)
        return Response(
            "You do not have permission to update Education for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        """Check if the user can update education and update education.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update education.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            "You do not have permission to partially update Education for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        """Check if the user can delete education and delete education.
        :param request:
        :param *args:
        :param **kwargs:
        :return: delete education.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response(
            "You do not have permission to delete Education for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )


class CertificationViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions."""

    queryset = Certification.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Serializer classes on specific action methods."""
        if self.action in ['create']:
            return CreateCertificationSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateCertificationSerializer
        return GetCertificationSerializer

    def create(self, request, *args, **kwargs):
        """Check if the user can create certification and create certifications.
        :param request:
        :param *args:
        :param **kwargs:
        :return: create certifications.
        """
        if request.data.get('person') != str(request.user.id):
            raise PermissionDenied("You do not have permission to add Certification for another user.")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Check if the user can update certification and update certifications.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update certifications.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().update(request, *args, **kwargs)
        return Response(
            "You do not have permission to update Certification for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        """Check if the user can update certification and update certifications.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update certifications.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            "You do not have permission to partially update Certification for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        """Check if the user can delete certification and delete certifications.
        :param request:
        :param *args:
        :param **kwargs:
        :return: delete certifications.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response(
            "You do not have permission to delete Certification for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )


class CourseViewSet(viewsets.ModelViewSet):
    """A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions."""

    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Serializer classes on specific action methods."""
        if self.action in ['create']:
            return CreateCourseSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateCoursesSerializer
        return GetCourseSerializer

    def create(self, request, *args, **kwargs):
        """Check if the user can delete course and delete course.
        :param request:
        :param *args:
        :param **kwargs:
        :return: create course.
        """
        if request.data.get('person') != str(request.user.id):
            raise PermissionDenied("You do not have permission to add Course for another user.")

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Check if the user can update course and delete course.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update course.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().update(request, *args, **kwargs)
        return Response(
            "You do not have permission to update Course for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def partial_update(self, request, *args, **kwargs):
        """Check if the user can update course and update course.
        :param request:
        :param *args:
        :param **kwargs:
        :return: update course.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            "You do not have permission to partially update Course for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        """Check if the user can delete course and delete course.
        :param request:
        :param *args:
        :param **kwargs:
        :return: delete course.
        """
        instance = self.get_object()
        if instance.person.user == request.user:
            return super().destroy(request, *args, **kwargs)
        return Response(
            "You do not have permission to delete Course for others profile.",
            status=status.HTTP_403_FORBIDDEN
        )
