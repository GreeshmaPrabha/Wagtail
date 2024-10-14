from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from .blocks import *
from django.core.exceptions import ValidationError

# Create your models here.

class CategoryIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    max_count = 1 #only one page is allowed
    parent_page_types = ['home.HomePage']  # Adjust according to your site structure
    subpage_types = ['category_property.CategoryPage']  # Adjust according to your site structure
    class Meta:
        verbose_name = _("Category Index Page")
        verbose_name_plural = _("Category Index Pages")

#Property page
class CategoryPage(Page):
    # property_type = models.CharField(max_length=10, choices=[('rent', 'Rent'), ('buy', 'Buy')],default='rent', null=False, blank=False)
    category_details = StreamField([
        ('category_facilities', CategoryBlock()),     
        
    ], use_json_field=True, null=True, blank=True, min_num=1)
    
    content_panels = Page.content_panels + [
        # FieldPanel('property_type'),   
        FieldPanel('category_details'),
    ]

    parent_page_types = ['CategoryIndexPage']

    class Meta:
        verbose_name = _("Category Page")
        verbose_name_plural = _("Category Page")
    