from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from django.core.exceptions import ValidationError
from django.forms import Select

class CommunityNewPage(Page):
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

class ProjectNewPage(Page):
    community = models.ForeignKey(
        'CommunityNewPage',  # String reference to avoid circular import issues
        on_delete=models.SET_NULL,
        related_name='projects',
        null=True,  # Make the field nullable as suggested by the warning
        blank=True  # Make the field blankable as suggested by the warning
    )
    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('community'),
        FieldPanel('description'),
    ]

@register_snippet
class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

class PropertyDynPage(Page):
    community = models.ForeignKey(
        'CommunityNewPage',  # String reference to avoid circular import issues
        on_delete=models.SET_NULL,
        related_name='properties',
        null=True,  # Make the field nullable as suggested by the warning
        blank=True  # Make the field blankable as suggested by the warning
    )
    project = models.ForeignKey(
        'ProjectNewPage',  # String reference to avoid circular import issues
        on_delete=models.SET_NULL,
        related_name='properties',
        null=True,  # Make the field nullable as suggested by the warning
        blank=True  # Make the field blankable as suggested by the warning
    )
    category = models.ForeignKey(
        'PropertyCategory',  # String reference to avoid circular import issues
        on_delete=models.PROTECT,
        related_name='properties'
    )
    description = RichTextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square meters")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('community', widget=Select(attrs={'id': 'id_community'})),
            FieldPanel('project', widget=Select(attrs={'id': 'id_project'})),
        ], heading="Location"),
        FieldPanel('category'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('bedrooms'),
        FieldPanel('bathrooms'),
        FieldPanel('area'),
    ]

    def clean(self):
        super().clean()
        if self.project and self.project.community != self.community:
            raise ValidationError("The selected project must belong to the selected community.")

    class Meta:
        verbose_name_plural = "Properties"
