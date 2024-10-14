from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from mysite.constantvariables import convert_to_choices,TYPE, CURRENCY, STATUS, PROPERTY_TYPE
from wagtail.documents.blocks import DocumentChooserBlock
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BaseFaqBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, help_text=_("Add your question"))
    answer = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add your answer"))

    class Meta:
        # template = "blocks/base_text_block.html"
        icon = "help"
        label = "FAQ Block"

class FAQBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    points = blocks.ListBlock(BaseFaqBlock(), label="Add FAQ", help_text="Add frequently asked questions to this section")
    
    
class ContentBlock(blocks.StructBlock):
    description = blocks.CharBlock(max_length=500)
    
class DeveloperIconBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=True)
    


class IconBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=True, help_text="Choose an icon image")

class DescriptionIconsBlock(blocks.StructBlock):
    descriptions = blocks.StreamBlock([
        ('description', blocks.RichTextBlock(required=True, help_text="Add a description"))
    ], min_num=1, max_num=10)
    
    icons = blocks.StreamBlock([
        ('icon', IconBlock())
    ], min_num=1, max_num=10)

class FlexibleContentBlock(blocks.StreamBlock):
    description_icons = DescriptionIconsBlock()



            
    
class DeveloperBlock(blocks.StructBlock):
    # description = blocks.ListBlock(ContentBlock())
    # developer_icon = blocks.ListBlock(DeveloperIconBlock())
    description_icons = DescriptionIconsBlock()
    faq = FAQBlock(required=False, help_text=_("Add FAQs section"))
    
    
class TableContentBlock(blocks.StructBlock):
    banner_image = ImageChooserBlock(required=False)
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description  = blocks.RichTextBlock(editor='default', required=True, help_text=_("Add description in table format"))
    # project_coun

    class Meta:
        icon = "doc-full"
        label = _("Table Content Block")   