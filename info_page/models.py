from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel,PageChooserPanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
# from .blocks import *
from django.core.exceptions import ValidationError
from wagtail.admin.panels import TabbedInterface, TitleFieldPanel, ObjectList
from mysite.models import *
from .blocks import *
from .blogs import *


class InformationIndexPage(BasePage):    
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['info_page.MultiplePage','info_page.ContentPage', 'info_page.BlogLinkPage'] 
    class Meta:
        verbose_name = _("Information Index Page")
        verbose_name_plural = _("Information Index Pages")
        
        
class MultiplePage(BasePage):
    max_count = 10
    parent_page_types = ['info_page.InformationIndexPage']  
    subpage_types = ['info_page.ContentPage', 'info_page.BlogLinkPage'] 

    class Meta:
        verbose_name = _("Multiple Page")
        verbose_name_plural = _("Multiple Pages")
        
class ContentPage(BasePage, BannerMixin):  
    content = StreamField([
        ('partner_page_list_block', PartnerPageListBlock(group="Base Blocks")),
        ('base_text_block', BaseTextBlock(group="Base Blocks")),
        ('about_us_block', AboutUsBlock(group="Base Blocks")),
        ('team_list_block', TeamListBlock(group="Card Blocks")),
        ('team_description_block', TeamDescriptionBlock(group="Card Blocks")),
        ('agent_list_block', AgentListBlock(group="Card Blocks")),
        ('value_list_block', ValueListBlock(group="Card Blocks")),
        ('agent_description_block', AgentDescriptionBlock(group="Card Blocks")),
        ('contact_block', ContactBlock(group="Base Blocks")),
        ('podcast_block', PodcastBlock(group="Base Blocks")),      
        ('base_heading_block', BaseHeadingBlock(group="Base Blocks")),   

        #blog blocks
        ('link_block', LinkBlock(group="Card Blocks")),
        ('career_block', CareerBlock(group="Card Blocks")),
        ('event_awards_block', EventAwardsBlock(group="Card Blocks")),
        ('base_content_block', BaseContentBlock(group="Card Blocks")),
        ('market_trend_block',MarketTrendsBlock(group="Card Blocks")),
        ('video_block',VideoCardBlock(group="Card Blocks")),
        ('podcast_block', PodcastBlock(group="Card Blocks")),
        ('report_block',ReportsBlock(group="Card Blocks")),
        ('news_block',NewsBlock(group="Card Blocks")),
        ('media_block', MediaBlock(group="Card Blocks")),
        
    ], use_json_field=True)
    
    content_panels = BasePage.content_panels + BannerMixin.banner_panels + [
        FieldPanel('content'),
    ]

    # Restrict child pages
    subpage_types = []
    parent_page_types = ['info_page.InformationIndexPage','info_page.MultiplePage']

    class Meta:
        verbose_name = _("Content Page")
        verbose_name_plural = _("Content Pages")
        
        
class BlogLinkPage(BasePage, BannerMixin):  
    internal_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_("Select an internal page"),
    )
    
    content = StreamField([
        ('partner_page_list_block', PartnerPageListBlock(group="Base Blocks")),
        ('base_text_block', BaseTextBlock(group="Base Blocks")),
        ('about_us_block', AboutUsBlock(group="Base Blocks")),
        ('team_list_block', TeamListBlock(group="Swiper Blocks")),
        ('team_description_block', TeamDescriptionBlock(group="Card Blocks")),
        ('agent_list_block', AgentListBlock(group="Card Blocks")),
        ('value_list_block', ValueListBlock(group="Card Blocks")),
        ('agent_description_block', AgentDescriptionBlock(group="Card Blocks")),
        ('contact_block', ContactBlock(group="Base Blocks")),
        ('podcast_block', PodcastBlock(group="Base Blocks")),        
        ('base_heading_block', BaseHeadingBlock(group="Base Blocks")),        

        #blog blocks
        ('link_block', LinkBlock(group="Card Blocks")),
        ('career_block', CareerBlock(group="Card Blocks")),
        ('event_awards_block', EventAwardsBlock(group="Card Blocks")),
        ('text_block', BaseTextBlock(group="Card Block")),
        ('market_trend_block',MarketTrendsBlock(group="Card Block")),
        ('video_block',VideoCardBlock(group="Card Block")),
        ('podcast_block', PodcastBlock(group="Card Blocks")),
        ('report_block',ReportsBlock(group="Card Block")),
        ('news_block',NewsBlock(group="Card Block")),
        ('media_block', MediaBlock(group="Card Blocks")),
        
    ], use_json_field=True)
    
    content_panels = BasePage.content_panels + BannerMixin.banner_panels + [
        PageChooserPanel('internal_page', BLOG_INDEX_TARGETS),
        FieldPanel('content'),
    ]

    # Restrict child pages
    subpage_types = []
    parent_page_types = ['info_page.InformationIndexPage','info_page.MultiplePage']

    class Meta:
        verbose_name = _("Blog Link Page")
        verbose_name_plural = _("Blog Link Pages")