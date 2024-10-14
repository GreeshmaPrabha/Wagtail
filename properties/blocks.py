from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from mysite.constantvariables import convert_to_choices,TYPE, CURRENCY, STATUS, PROPERTY_TYPE
# from wagtail.fields import FileBlock
from wagtail.documents.blocks import DocumentChooserBlock


# mysite/mysite/constantvariables.py
    
# class ImageBlock(blocks.StructBlock):
    # image = ImageChooserBlock(required=False)
    
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

    def clean(self, value):
        cleaned_data = super().clean(value)
        if cleaned_data['media_type'] == 'image' and not cleaned_data['image']:
            raise blocks.ValidationError("An image is required.")
        if cleaned_data['media_type'] == 'video' and not cleaned_data['video']:
            raise blocks.ValidationError("A video file is required.")
        return cleaned_data
    
class ContentBlock(blocks.StructBlock):
    content_data = blocks.CharBlock(required=False, max_length=250)
    
    
class PropertyBlock(blocks.StructBlock):
    # property_images = blocks.ListBlock(ImageBlock())
    property_media = blocks.ListBlock(MediaBlock())
    property_type = blocks.ChoiceBlock(choices=convert_to_choices(PROPERTY_TYPE), label="Select Property Type")
    type_choice = blocks.ChoiceBlock(choices=convert_to_choices(TYPE), label="Select Type")
    amount = blocks.CharBlock(required=False, max_length=250)
    currency_type = blocks.ChoiceBlock(choices=convert_to_choices(CURRENCY), label="Select Currency")
    title = blocks.CharBlock(required=False, max_length=250)
    property = blocks.CharBlock(required=False, max_length=250)
    location = blocks.CharBlock(required=False, max_length=250)
    bedroom_count = blocks.CharBlock(required=False, max_length=250)
    bathroom_count = blocks.CharBlock(required=False, max_length=250)
    plot = blocks.CharBlock(required=False, max_length=250)
    whatsapp = blocks.CharBlock(required=False, max_length=250)
    call_contact = blocks.CharBlock(required=False, max_length=250)
    mortgage_description = blocks.CharBlock(required=False, max_length=250)
    sale_desc = blocks.CharBlock(required=False, max_length=250)
    bua_plot = blocks.CharBlock(required=False, max_length=250)
    plot_sqft = blocks.CharBlock(required=False, max_length=250)
    status = blocks.ChoiceBlock(choices=convert_to_choices(STATUS), label="Select Status")
    description_title = blocks.CharBlock(required=False, max_length=250)
    description = blocks.CharBlock(required=False, max_length=250)
    maid_apartment_title = blocks.CharBlock(required=False, max_length=250)
    maid_apartment_content = blocks.ListBlock(ContentBlock()) 