from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core-app/', include('core.urls')),
    path('feeds-app/', include('feed.urls')),
    path('jobs-app/', include('job.urls')),
]
