from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet, UserRegistrationView, ChangePasswordView, UpdateUserView, LogoutAllView,
    LogoutView, FollowCreateView, UnfollowView, UserListView, UserDeleteView, FollowerListView,
    FollowingListView, ExperienceViewSet, EducationViewSet, CertificationViewSet, CourseViewSet
)

app_name = 'core'

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('register/register-user/', UserRegistrationView.as_view(), name='register'),

    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/list-users/', UserListView.as_view(), name='user-list'),
    path('user/delete-user/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),

    path('user/change-password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
    path('user/update-user/<int:pk>/', UpdateUserView.as_view(), name='Update_profile'),

    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('user/logout-all/', LogoutAllView.as_view(), name='logout_all'),

    path('', include(router.urls)),

    path('follow-profile/follow-user/', FollowCreateView.as_view(), name='follow-create'),
    path('follow-profile/followers/', FollowerListView.as_view(), name='follower-list'),
    path('follow-profile/following/', FollowingListView.as_view(), name='following-list'),
    path('follow-profile/unfollow-user/<int:profile_id>/', UnfollowView.as_view(), name='follow-delete'),

    path('profile-details/', include(router.urls)),
]
