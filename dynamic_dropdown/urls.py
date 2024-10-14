
from django.urls import path
from .views import get_projects

urlpatterns = [
    path('projects/<int:community_id>/', get_projects, name='get_projects'),
]