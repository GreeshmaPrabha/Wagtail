from django.http import JsonResponse
from .models import ProjectNewPage

def projects_by_community(request, community_id):
    projects = ProjectNewPage.objects.filter(community_id=community_id).values_list('id', 'title')
    return JsonResponse(dict(projects))