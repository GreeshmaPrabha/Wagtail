from django.db import models

# Create your models here.
from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _


class CommunityDynamic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ProjectDynamic(models.Model):
    name = models.CharField(max_length=255)
    community = models.ForeignKey(CommunityDynamic, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name

class PropertyDynamicPage(Page):
    community = models.ForeignKey(CommunityDynamic, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(ProjectDynamic, on_delete=models.SET_NULL, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('community'),
        FieldPanel('project'),
    ]

    class Meta:
        verbose_name = _("Property Dynamic Page")
        verbose_name_plural = _("Property Dynamic Pages")
        
        