from django.http import JsonResponse
from .models import ProjectDynamic

def get_projects(request, community_id):
    projects = ProjectDynamic.objects.filter(community_id=community_id).values('id', 'name')
    project_list = list(projects)  # Convert to list of dicts
    return JsonResponse(project_list, safe=False)