from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from .blocks import *
from django.core.exceptions import ValidationError

# Create your models here.

class AmenitiesIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    max_count = 1 #only one page is allowed
    parent_page_types = ['home.HomePage']  # Adjust according to your site structure
    subpage_types = ['amenities.AmenitiesPage']  # Adjust according to your site structure
    class Meta:
        verbose_name = _("Amenities New Index Page")
        verbose_name_plural = _("Amenities New Index Pages")

#Property page
class AmenitiesPage(Page):
    heading = models.CharField(null=False, blank=False, max_length=250)
    facilities = StreamField([
        ('amenities_facilities', AmenitiesBlock()),     
        
    ], use_json_field=True, null=True, blank=True,max_num=1, min_num=1)
    
    content_panels = Page.content_panels + [
        FieldPanel('heading'),   
        FieldPanel('facilities'),
    ]

    parent_page_types = ['AmenitiesIndexPage']

    class Meta:
        verbose_name = _("Amenities Page")
        verbose_name_plural = _("Amenities Page")
    