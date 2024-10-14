from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from mysite.constantvariables import convert_to_choices,TYPE, CURRENCY, STATUS, PROPERTY_TYPE
from wagtail.documents.blocks import DocumentChooserBlock
from django.core.exceptions import ValidationError


class ContentBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False, max_length=250)
    
    
class AmenitiesBlock(blocks.StructBlock):
    facilities_amenities = blocks.ListBlock(ContentBlock())