from django.db import models
from wagtail.snippets.models import register_snippet
# from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail import blocks


@register_snippet
class DeveloperSnippet(models.Model):
    developer_title = models.CharField(max_length=255)
    # content = models.TextField(required=False)
    icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    panels = [
        FieldPanel('developer_title'),
        # FieldPanel('content'),
        FieldPanel('icon'),
    ]
    
    def __str__(self):
        return self.developer_title

class ProjectPage(models.Model):  # This is an example parent model
    snippets = StreamField([
        ('developer_snippet', blocks.StructBlock([
            ('snippet', blocks.ChooserBlock(DeveloperSnippet, label="Developer Snippet")),
        ])),
    ])

    content_panels = [
        FieldPanel('snippets'),
    ]
    
    
@register_snippet
class CategorySnippet(models.Model):
    category_title = models.CharField(max_length=255)
    category_content = models.TextField(max_length=255)
    # icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    panels = [
        FieldPanel('category_title'),
        FieldPanel('category_content'),
        # FieldPanel('icon'),
    ]
    
    def __str__(self):
        return self.category_title