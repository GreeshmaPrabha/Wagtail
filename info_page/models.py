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
        # base
        ('base_content_block', BaseContentBlock(group="Base Blocks")),
        ('overlayed_image_block', OverlayedImageBlock(group="Base Blocks")),
        ('normal_image_block', NormalImageBlock(group="Base Blocks")),
        ('management_msg_block', ManagementMessageBlock(group="Base Blocks")),
        ('top_management_block', TopManagementListBlock(group="Base Blocks")),
        ('management_list_block', ManagementListBlock(group="Base Blocks")),
        ('base_image_block', BaseImageBlock(group="Base Blocks")),
        ('normal_text', NormalTextBlock(group="Base Blocks")),        
        ('feature_list_block', FeaturesListBlock(group="Base Blocks")),        
        ('point_text_block', PointTextBlock(group="Base Blocks")),        
        ('why_us_block', WhyUsBlock(group="Base Blocks")), 
        ('overview_block', OverviewBlock(group="Base Blocks")), 
        ('contact_info_block', ContactInfoBlock(group="Base Blocks")),        
        ('social_share_block', SocialSharingBlock(group="Base Blocks")),
        ('link_block', LinkBlock(group="Base Blocks")),        
        ('faq_block', FAQBlock(group="Base Blocks")),
        ('related_news', RelatedNewsBlock(group="Base Blocks")),
        ('project_list', ProjectListBlock(group="Base Blocks")),        
        ('property_list', PropertyListBlock(group="Base Blocks")),
        ('agent_list', AgentListBlock(group="Base Blocks")),
        ('developer_list', DeveloperListBlock(group="Base Blocks")),
        ('overlayed_image_multi_data_list', MultiContentOverlayedBlock(group="Base Blocks")),
        ('single_image_multi_data_list', MultiContentImageBlock(group="Base Blocks")),
        
        # card
        ('review_card_block', ReviewCardBlock(group="Card Blocks")),
        ('image_card_block', ImageCardBlock(group="Card Blocks")),
        ('text_card_block', TextCardBlock(group="Card Blocks")),        
        ('profile_card_block', ProfileCardBlock(group="Card Blocks")),
        ('info_card_block', InfoCardBlock(group="Card Blocks")),
        
        
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
        # base
        ('base_content_block', BaseContentBlock(group="Base Blocks")),
        ('overlayed_image_block', OverlayedImageBlock(group="Base Blocks")),
        ('normal_image_block', NormalImageBlock(group="Base Blocks")),
        ('management_msg_block', ManagementMessageBlock(group="Base Blocks")),
        ('top_management_block', TopManagementListBlock(group="Base Blocks")),
        ('management_list_block', ManagementListBlock(group="Base Blocks")),
        ('base_image_block', BaseImageBlock(group="Base Blocks")),
        ('normal_text', NormalTextBlock(group="Base Blocks")),        
        ('feature_list_block', FeaturesListBlock(group="Base Blocks")),        
        ('point_text_block', PointTextBlock(group="Base Blocks")),        
        ('why_us_block', WhyUsBlock(group="Base Blocks")), 
        ('overview_block', OverviewBlock(group="Base Blocks")), 
        ('contact_info_block', ContactInfoBlock(group="Base Blocks")),        
        ('social_share_block', SocialSharingBlock(group="Base Blocks")),
        ('link_block', LinkBlock(group="Base Blocks")),        
        ('faq_block', FAQBlock(group="Base Blocks")),
        ('related_news', RelatedNewsBlock(group="Base Blocks")),
        ('project_list', ProjectListBlock(group="Base Blocks")),
        ('property_list', PropertyListBlock(group="Base Blocks")),
        ('agent_list', AgentListBlock(group="Base Blocks")),
        ('developer_list', DeveloperListBlock(group="Base Blocks")),
        ('overlayed_image_multi_data_list', MultiContentOverlayedBlock(group="Base Blocks")),
        ('single_image_multi_data_list', MultiContentImageBlock(group="Base Blocks")),
        
        # card
        ('review_card_block', ReviewCardBlock(group="Card Blocks")),
        ('image_card_block', ImageCardBlock(group="Card Blocks")),
        ('text_card_block', TextCardBlock(group="Card Blocks")),        
        ('profile_card_block', ProfileCardBlock(group="Card Blocks")),
        ('info_card_block', InfoCardBlock(group="Card Blocks")),
        
        
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