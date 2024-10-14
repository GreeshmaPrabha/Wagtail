from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from mysite.utils import get_image_rendition
from info_page.blogs import *
from info_page.blocks import *
from mysite.models import BasePage, BannerMixin


# This is the index page for awards. It inherits from BasePage and BannerMixin.
# It holds introductory and body content and has a max count restriction of 1 page.
class AwardsIndexPage(BasePage, BannerMixin):
    # Intro and body fields for the page content
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    # Panels for admin interface configuration, extending the base content panels
    content_panels = BasePage.content_panels + BannerMixin.banner_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    max_count = 1  # Only one instance of this page is allowed
    parent_page_types = ['home.HomePage']  # This page can only be created under HomePage
    subpage_types = ['events_awards.AwardsPage']  # Only AwardPage can be created as a subpage

    class Meta:
        verbose_name = _("Awards Index Page")
        verbose_name_plural = _("Awards Index Pages")


# Model for tagging AwardsPage using Wagtail's tagging system
class AwardsPageTag(TaggedItemBase):
    # Relation to AwardsPage model
    content_object = ParentalKey(
        'AwardsPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# Mixin to keep track of the view count of AwardPages
class ViewCountMixin(models.Model):
    view_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True  # This makes it a mixin, not a standalone model


# The main AwardsPage model that contains all content for individual award posts
class AwardsPage(ViewCountMixin, BasePage, BannerMixin):
    # Date, author (using StreamField), and reading time fields
    heading = models.CharField(_("Heading"),null=True, blank=True, max_length=250)
    awards = StreamField([
        ('awards_block', EventAwardsBlock())
    ], use_json_field=True,  null=True,blank=True,min_num=0) #max_num=1
    # AccoladesBlock
    accolades_heading = models.CharField(_("Accolades Heading"),null=True, blank=True, max_length=250)
    
    accolades = StreamField([
        ('accolades_block', EventAwardsBlock())
    ], use_json_field=True,  null=True,blank=True,min_num=0)

    # Introductory text and banner image for the award page
    # intro = RichTextField(blank=True)
    # banner_image = models.ForeignKey(
    #     "wagtailimages.Image",
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="+",
    #     help_text=_("Banner image"),
    # )

    # Tagging system for the page
    tags = ClusterTaggableManager(through=AwardsPageTag, blank=True)

    # Fields indexed for search functionality
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('awards'),
    ]

    # Admin interface panels, allowing users to edit the award page details
    content_panels = BasePage.content_panels + BannerMixin.banner_panels + [
        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel("awards"),
            FieldPanel("accolades_heading"),
            FieldPanel("accolades"),
            FieldPanel('tags'),
        ], heading="Awards information"),
    ]

    # No child pages allowed for AwardPage
    subpage_types = []

    # Must be created under AwardIndexPage
    parent_page_types = ['events_awards.AwardsIndexPage']

    # Method to get the main image for the page
    @property
    def main_image_data(self):
        return get_image_rendition(self.banner_image, 'original')

    # Method to increment view count when the page is accessed
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    class Meta:
        verbose_name = _("Awards Page")
        verbose_name_plural = _("Awards Pages")



