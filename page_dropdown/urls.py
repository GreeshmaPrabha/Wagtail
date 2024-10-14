from django.urls import path
from .views import projects_by_community

urlpatterns = [
    path('projects-by-community/<int:community_id>/', projects_by_community, name='projects_by_community'),
]