from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from .blocks import *
from django.core.exceptions import ValidationError
from category_property.models import *
# from wagtail_dynamic_dropdown import DynamicDropdownField
from wagtail_dynamic_dropdown.edit_handlers import DynamicDropdownPanel
from .custom_panel import CustomDynamicDropdownPanel
from wagtail.admin.panels import TabbedInterface, TitleFieldPanel, ObjectList




# Create your models here.

class PropertyNewIndexPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    max_count = 1 #only one page is allowed
    parent_page_types = ['home.HomePage']  # Adjust according to your site structure
    subpage_types = ['property_new.PropertyNewPage']  # Adjust according to your site structure
    class Meta:
        verbose_name = _("Property New Index Page")
        verbose_name_plural = _("Property New Index Pages")

#Property page
class PropertyNewPage(Page):    
    PROPERTY_TYPE = [
        ('1', _('Apartment')),
        ('2', _('Commercial-Floors')),
        ('3', _('Duplexs')),
        ('4', _('Hotel-Apartments')),
        ('5', _('Offices')),
        ('6', _('Penthouses')),       
    ]
    TYPE = [
        ('1', _('Rent')),
        ('2', _('Buy')),    
    ]
    CURRENCY = [
        ('1', _('AED')),
        ('2', _('BHD')),
        ('3', _('KWD')),
        ('4', _('OMR')),
        ('5', _('QAR')),
        ('6', _('SAR')),      
    ]
    
    STATUS = [
        ('1', _('Completed')),
        ('2', _('Pending')),
        ('3', _('Inprogress')),  
    ]
    MORTGAGE_TYPE = [
        ('1', _('Months')),
        ('2', _('Years')),  
    ]
    

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE,  null=True, blank=True)    
    category = models.ForeignKey(CategoryPage, on_delete=models.SET_NULL, null=True, blank=True)

    # sub_category = models.CharField(max_length=255, blank=True)    
    type_choice = models.CharField(max_length=20, choices=TYPE,  null=True, blank=True)    
    amount = models.CharField( null=True, blank=True, max_length=250)
    currency_type = models.CharField(max_length=20, choices=CURRENCY,  null=True, blank=True)
    property_title = models.CharField( null=True, blank=True, max_length=250)
    property = models.CharField( null=True, blank=True, max_length=250)
    location = models.CharField( null=True, blank=True, max_length=250)
    bedroom_count = models.CharField( null=True, blank=True, max_length=250)
    bathroom_count = models.CharField( null=True, blank=True, max_length=250)
    plot = models.CharField( null=True, blank=True, max_length=250)
    whatsapp = models.CharField( null=True, blank=True, max_length=250)
    call_contact = models.CharField( null=True, blank=True, max_length=250)
    mortgage_description = models.CharField( null=True, blank=True, max_length=250)
    mortgage_duration_type = models.CharField(max_length=20, choices=MORTGAGE_TYPE,  null=True, blank=True)
    mortgage_duration = models.CharField( null=True, blank=True, max_length=250)
    sale_desc = models.CharField( null=True, blank=True, max_length=250)
    bua_plot = models.CharField( null=True, blank=True, max_length=250)
    plot_sqft = models.CharField( null=True, blank=True, max_length=250)
    status = models.CharField(max_length=20, choices=STATUS,  null=True, blank=True)
    description_title = models.CharField( null=True, blank=True, max_length=250)
    description =models.CharField( null=True, blank=True, max_length=250)
    maid_apartment_title = models.CharField( null=True, blank=True, max_length=250)
    
    image_content = StreamField([
        ('property_new_block', PropertyImageBlock()),     
        
    ], use_json_field=True, null=True, blank=True,max_num=1, min_num=1)
    
    maid_content = StreamField([
        ('property_new_maid_content_block', PropertyMaidContentBlock()),        
    ], use_json_field=True, null=True, blank=True,max_num=1, min_num=1)
    
    data_block = StreamField([
        ('data_block', PropertyDataBlock()),     
        
    ], use_json_field=True, null=True, blank=True,max_num=1, min_num=1)
    
    location_block = StreamField([
        ('location_block', LocationBlock()),     
        
    ], use_json_field=True, null=True, blank=True,max_num=1, min_num=1)
    
    
    def get_dynamic_categories(self):
        """Return categories based on the selected property type."""
        if self.property_type == '1':
            return CategoryPage.objects.filter(is_rent=True).values_list('id', 'category_name')
        elif self.property_type == '2':
            return CategoryPage.objects.filter(is_buy=True).values_list('id', 'category_name')
        return CategoryPage.objects.none()  # Return empty if no type selected
    

    content_panels = Page.content_panels + [
        FieldPanel('image_content'),
        FieldPanel('maid_content'),
        FieldPanel('property_type'),
        # CustomDynamicDropdownPanel(
        #     'category',
        #     dynamic_choices=lambda instance: instance.get_dynamic_categories()
        # ),
        # # DynamicDropdownPanel('sub_category', model=CategoryPage), 
        FieldPanel('category'),     
        # FieldPanel('sub_category'), 
        FieldPanel('type_choice'),
        # FieldPanel('amount'),        
        # FieldPanel('currency_type'),
        FieldPanel('property_title'),
        FieldPanel('property'),
        FieldPanel('location'),
        FieldPanel('location_block'),        
        FieldPanel('data_block'),
        FieldPanel('whatsapp'),
        FieldPanel('call_contact'),
        FieldPanel('mortgage_description'),
        FieldPanel('mortgage_duration_type'),
        FieldPanel('mortgage_duration'),
        FieldPanel('sale_desc'),
        FieldPanel('bua_plot'),
        FieldPanel('plot_sqft'),
        FieldPanel('status'),
        FieldPanel('description_title'),
        FieldPanel('description'),
        FieldPanel('maid_apartment_title'),
    ]
    
    sidebar_content_panels = [
        FieldPanel('amount'),        
        FieldPanel('currency_type'),
    ]
    
    
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(sidebar_content_panels, heading='Amount'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings'), # The default settings are now displayed in the sidebar but need to be in the `TabbedInterface`.
    ])
    

    parent_page_types = ['PropertyNewIndexPage']
    
    class Meta:
        verbose_name = _("Property New Page")
        verbose_name_plural = _("Property New Page")   
        
    # def get_context(self, request):
    #     context = super().get_context(request)
    #     context['dynamic_categories'] = self.get_dynamic_categories()  # Call method on the instance
    #     return context
        
class FavouriteProperty(models.Model):
    user = models.CharField(null=True, blank=True, max_length=250)
    property = models.ForeignKey(PropertyNewPage, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ('user', 'property')  # Prevent duplicate favorites
