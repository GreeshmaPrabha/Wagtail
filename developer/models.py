from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from .blocks import *
from django.core.exceptions import ValidationError
from wagtail.admin.panels import TabbedInterface, TitleFieldPanel, ObjectList
from masters.models import *


# Create your models here.

class DeveloperIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    max_count = 1 #only one page is allowed
    parent_page_types = ['home.HomePage']  # Adjust according to your site structure
    subpage_types = ['developer.DeveloperPage']  # Adjust according to your site structure
    class Meta:
        verbose_name = _("Developer Index Page")
        verbose_name_plural = _("Developer Index Pages")

#Property page
class DeveloperPage(Page):
    banner_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='developer_banner_image')
    banner_heading = models.CharField(max_length=255) 
    developer_details = StreamField([
        ('developer_detail', DeveloperBlock()),     
        
    ], use_json_field=True, null=True, blank=True, min_num=1)
    
    developer_detail_page = StreamField([
        ('detail_content', TableContentBlock()),     
        
    ], use_json_field=True, null=True, blank=True, min_num=1)
    
    developers = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True, related_name='developer_pages')
    
    content_panels = Page.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('banner_heading'),
        FieldPanel('developer_details'),
    ]
    
    sidebar_content_panels = [
        FieldPanel('developer_detail_page'),
        FieldPanel('developers'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Developer Detail'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'), # The default settings are now displayed in the sidebar but need to be in the `TabbedInterface`.
    ])
    
    parent_page_types = ['DeveloperIndexPage']

    class Meta:
        verbose_name = _("Developer Page")
        verbose_name_plural = _("Developer Page")
    