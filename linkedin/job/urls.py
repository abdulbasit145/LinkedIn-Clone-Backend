from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import JobPostViewSet, JobApplicationViewSet


app_name = "job"


router = DefaultRouter()
router.register(r'jobs', JobPostViewSet)
router.register(r'applications', JobApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
