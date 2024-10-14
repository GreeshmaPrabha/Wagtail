from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from mysite.constantvariables import convert_to_choices,TYPE, CURRENCY, STATUS, PROPERTY_TYPE
# from wagtail.fields import FileBlock
from wagtail.documents.blocks import DocumentChooserBlock
from django.core.exceptions import ValidationError

class MediaWith360Block(blocks.StructBlock):
    order = blocks.IntegerBlock(required=False,min_value=1)
    image = ImageChooserBlock(required=False)

class MediaBlock(blocks.StructBlock):
    media_type = blocks.ChoiceBlock(
        choices=[
            ('image', 'Image'),
            ('video', 'Video'),
        ],
        default='image',
    )
    image = ImageChooserBlock(required=False)
    video = DocumentChooserBlock(required=False)
    is_base = blocks.BooleanBlock(required=False, default=False, help_text="Check if this is the base media.")

    def clean(self, value):
        cleaned_data = super().clean(value)

        # Ensure only one media type is uploaded
        if cleaned_data['media_type'] == 'image':
            if not cleaned_data['image']:
                raise ValidationError("An image is required when 'Image' is selected.")
            if cleaned_data['video']:
                raise ValidationError("No video should be provided when 'Image' is selected.")
        elif cleaned_data['media_type'] == 'video':
            if not cleaned_data['video']:
                raise ValidationError("A video file is required when 'Video' is selected.")
            if cleaned_data['image']:
                raise ValidationError("No image should be provided when 'Video' is selected.")

        # Ensure only one base media is designated
        if cleaned_data['is_base']:
            if cleaned_data['media_type'] == 'image' and not cleaned_data['image']:
                raise ValidationError("Cannot set base media as image when no image is provided.")
            if cleaned_data['media_type'] == 'video' and not cleaned_data['video']:
                raise ValidationError("Cannot set base media as video when no video is provided.")

        return cleaned_data

    # def clean(self, value):
    #     cleaned_data = super().clean(value)
    #     if cleaned_data['media_type'] == 'image' and not cleaned_data['image']:
    #         raise ValidationError("An image is required.")
    #     if cleaned_data['media_type'] == 'video' and not cleaned_data['video']:
    #         raise ValidationError("A video file is required.")
    #     return cleaned_data
    
class ContentBlock(blocks.StructBlock):
    content_data = blocks.CharBlock(required=False, max_length=250)
    
class ContactBlock(blocks.StructBlock):
    content_data = blocks.CharBlock(required=False, max_length=250)
    
    
class DataContentBlock(blocks.StructBlock):
    icon = ImageChooserBlock(required=False)
    title = blocks.CharBlock(required=False, max_length=250)
    content = blocks.CharBlock(required=False, max_length=250)
    
class PropertyImageBlock(blocks.StructBlock):
    # property_images = blocks.ListBlock(ImageBlock())
    property_media_with_360 = blocks.ListBlock(MediaWith360Block())
    property_media = blocks.ListBlock(MediaBlock())

class PropertyMaidContentBlock(blocks.StructBlock):
    maid_apartment_content = blocks.ListBlock(ContentBlock()) 
    

class PropertyDataBlock(blocks.StructBlock):
    data_content = blocks.ListBlock(DataContentBlock()) 
    
class LocationBlock(blocks.StructBlock):
    location_name = blocks.CharBlock(required=False, max_length=250)
    latitude = blocks.CharBlock(required=False, max_length=250)
    longitude = blocks.CharBlock(required=False, max_length=250)
    
class ContactPersonBlock(blocks.StructBlock):
    contact_person_content = blocks.ListBlock(ContactBlock()) 