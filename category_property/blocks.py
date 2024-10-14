from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from mysite.constantvariables import convert_to_choices,TYPE, CURRENCY, STATUS, PROPERTY_TYPE
from wagtail.documents.blocks import DocumentChooserBlock
from django.core.exceptions import ValidationError


class ContentBlock(blocks.StructBlock):
    sub_category = blocks.CharBlock(max_length=250)

class PropertyTypeBlock(blocks.ChoiceBlock):
    def __init__(self, *args, **kwargs):
        choices = [
            ('rent', 'Rent'),
            ('buy', 'Buy')
        ]
        super().__init__(choices=choices, *args, **kwargs)
            
    
class CategoryBlock(blocks.StructBlock):
    property_type = PropertyTypeBlock()
    category = blocks.CharBlock(max_length=250)
    sub_category = blocks.ListBlock(ContentBlock())