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


# This is the index page for carees. It inherits from BasePage and BannerMixin.
# It holds introductory and body content and has a max count restriction of 1 page.
class CareerIndexPage(BasePage, BannerMixin):
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
    subpage_types = ['career.CareerPage']  # Only AwardPage can be created as a subpage

    class Meta:
        verbose_name = _("Career Index Page")
        verbose_name_plural = _("Career Index Pages")


# Model for tagging CareerPages using Wagtail's tagging system
class CareerPageTag(TaggedItemBase):
    # Relation to CareerPage model
    content_object = ParentalKey(
        'CareerPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# Mixin to keep track of the view count of AwardPages
class ViewCountMixin(models.Model):
    view_count = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        abstract = True  # This makes it a mixin, not a standalone model


# The main CareerPage model that contains all content for individual award posts
class CareerPage(ViewCountMixin, BasePage, BannerMixin):
    
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Career image"),
    )
    heading = models.CharField(_("Career heading"), null=True, blank=True, max_length=100)
    posted_date = models.DateField(_("Posted date"), null=True, blank=True)
    expiry_date = models.DateField(_("Expiry date"), null=True, blank=True)
    description = RichTextField(_("Description"), blank=True) 
    location = models.CharField(_("location"), null=True, blank=True, max_length=100)
    tags = ClusterTaggableManager(through=CareerPageTag, blank=True)

    # StreamField for the main content of the page, restricted to 1 content_block and 1 trade_block
    # content = StreamField([
    #     ('career_block', ImageCardBlock(group="Base Blocks")),
    #     ('career_opening_block', BaseContentBlock(group="Base Blocks")),
        
    # ], use_json_field=True,  null=True,blank=True,min_num=0, block_counts={
    #     'career_block': {'min_num': 0},
    #     'career_opening_block': {'min_num': 0},
    # })

    # Fields indexed for search functionality
    search_fields = Page.search_fields + [
        index.SearchField('heading'),
        index.SearchField('posted_date'),
        index.SearchField('description'),
    ]    
    content_panels = BasePage.content_panels + BannerMixin.banner_panels + [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('heading'),
            FieldPanel('posted_date'),
            FieldPanel("expiry_date"),
            FieldPanel('description'),
            FieldPanel('location'),
            FieldPanel('tags'),
        ], heading="Career information"),
        # FieldPanel('content'),
    ]

    # No child pages allowed for AwardPage
    subpage_types = []

    # Must be created under AwardIndexPage
    parent_page_types = ['career.CareerIndexPage']

    # Method to get the main image for the page
    @property
    def main_image_data(self):
        return get_image_rendition(self.banner_image, 'original')

    # Method to increment view count when the page is accessed
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    class Meta:
        verbose_name = _("Career Page")
        verbose_name_plural = _("Career Pages")



