from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from .blocks import *
from django.core.exceptions import ValidationError

# Create your models here.

class PropertyIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    max_count = 1 #only one page is allowed
    parent_page_types = ['home.HomePage']  # Adjust according to your site structure
    subpage_types = ['properties.PropertyPage']  # Adjust according to your site structure
    class Meta:
        verbose_name = _("Property Index Page")
        verbose_name_plural = _("Property Index Pages")

#Property page
class PropertyPage(Page):    
    content = StreamField([
        ('property_block', PropertyBlock()),
        
    ], use_json_field=True, max_num=1, min_num=1)
    #, max_num=1, min_num=1
    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    parent_page_types = ['PropertyIndexPage']

    class Meta:
        verbose_name = _("Property Page")
        verbose_name_plural = _("Property Page")
        