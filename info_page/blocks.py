from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from mysite.constantvariables import *



class VideoCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    video_source = blocks.ChoiceBlock(
        choices=[
            ('upload', 'Upload Video'),
            ('external', 'External Video Link'),
        ],
        label="Video Source",
        help_text="Choose whether to upload a video or provide an external link."
    )

    uploaded_video = DocumentChooserBlock(
        required=False,
        label="Upload Video",
        help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
    )
    external_video_link = blocks.URLBlock(
        required=False,
        label="External Video Link",
        help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
    )   

    watch_time = blocks.IntegerBlock(
        label="Watch Time (minutes)",
        help_text="Estimated time to watch/read the content.",
        required=False
    )

    proficiency_level = blocks.ChoiceBlock(
        choices=PROFICIENCY_LEVEL_CHOICES,
        label="Proficiency Level",
        help_text="Select the difficulty level."
    )

    thumbnail = ImageChooserBlock(
        label="Thumbnail Image",
        help_text="Choose a thumbnail image for the video."
    )

    link_label = blocks.CharBlock(
        label="Link Label",
        max_length=50,
        help_text="The text for the link button.",
        required=False
    )

    class Meta:
        icon = "media"
        label = _("Video Block")

    def clean(self, value):
        cleaned_data = super().clean(value)
        video_source = cleaned_data.get('video_source')
        uploaded_video = cleaned_data.get('uploaded_video')
        external_video_link = cleaned_data.get('external_video_link')

        if video_source == 'upload':
            if not uploaded_video:
                raise ValidationError({'uploaded_video': 'Please upload a video file.'})
            else:
                # Check if the uploaded file is a video
                allowed_extensions = ['mp4', 'mov', 'avi', 'webm']
                file_extension = uploaded_video.file_extension.lower().lstrip('.')
                if file_extension not in allowed_extensions:
                    raise ValidationError({'uploaded_video': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'})
        elif video_source == 'external' and not external_video_link:
            raise ValidationError({'external_video_link': 'Please provide an external video link.'})

        # Prevent both internal and external links from being filled
        if video_source == 'upload' and external_video_link:
            raise ValidationError(_('An external URL should not be provided when video source is upload.'))
        if video_source == 'external' and uploaded_video:
            raise ValidationError(_('An video should not be provided when video source is external.'))

        return cleaned_data
    

class LinkBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=False, help_text=_("Enter the label of the link"))
    link_type = blocks.ChoiceBlock(
        choices = [
            ('internal', _('Internal Page')),
            ('external', _('External URL')),
        ],
        default='internal',
        help_text=_("Select the type of link"),
    )
    internal_page = blocks.PageChooserBlock(
        required=False, 
        help_text=_("Select an internal page"),
        target_model = PAGE_TARGETS
    )
    external_url = blocks.URLBlock(
        required=False, 
        help_text=_("Enter an external URL"),
    )

    def clean(self, value):
        """
        Custom validation to ensure that only one type of link (internal or external) is provided,
        and that the appropriate fields are filled based on the selected link type.
        """
        cleaned_data = super().clean(value)
        link_type = cleaned_data.get('link_type')
        internal_page = cleaned_data.get('internal_page')
        external_url = cleaned_data.get('external_url')

        # Validation logic based on link type
        if link_type == 'internal' and not internal_page:
            raise ValidationError(_('An internal page must be selected when "Internal Page" is chosen.'))
        elif link_type == 'external' and not external_url:
            raise ValidationError(_('A URL must be provided when "External URL" is chosen.'))

        # Prevent both internal and external links from being filled
        if link_type == 'internal' and external_url:
            raise ValidationError(_('An external URL should not be provided when linking to an internal page.'))
        if link_type == 'external' and internal_page:
            raise ValidationError(_('An internal page should not be provided when linking to an external URL.'))

        return cleaned_data
    
    class Meta:
        label = _("Link Information")
        icon = 'link'
        

class BaseFaqBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, help_text=_("Add your question"))
    answer = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add your answer"))

    class Meta:
        icon = "help"
        label = _("Base FAQ Block")

class FAQBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    points = blocks.ListBlock(BaseFaqBlock(), label="Add FAQ", help_text="Add frequently asked questions to this section")
    
    class Meta:
        icon = "help"
        label = "FAQ Block"
    
    
class BaseContentBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class Meta:
        icon = "doc-full"
        label = "Content Block"        
        
#  ----------------------------------- ----------------------------------- ----------------------------------- -----------------------------------

class OverlayedImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    main_image = ImageChooserBlock(required=True)    
    secondary_image = ImageChooserBlock(required=True)    
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    image_alignment = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="center", help_text=_("Block Alignment"))
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    
    class Meta:
        icon = "image"
        label = _("Overlayed Image Block")
    
class ImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    image = ImageChooserBlock(required=False)
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    image_alignment = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="center", help_text=_("Block Alignment"))
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))

    class meta:
        icon = "image"
        label = _("Image Block")
        
class ImageCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    image = ImageChooserBlock(required=True)
    
    
    class Meta:
        icon = "image"
        label = _("Image block with cards")
        
class TextCardBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class Meta:
        icon = "doc-full"
        label = _("Text block with cards")

class NormalImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    points = blocks.ListBlock(ImageCardBlock(),label="Add image cards", help_text="Add image cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Normal Image Block")

class ManagementMessageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    name = blocks.CharBlock(required=False, help_text=_("Add name"))
    designation = blocks.CharBlock(required=False, help_text=_("Add designation"))
    message = blocks.RichTextBlock(required=False)
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    
    class Meta:
        icon = "doc-full"
        label = _("Management Message Block")
    
class ProfileCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    name = blocks.CharBlock(required=False, help_text=_("Add name"))
    designation = blocks.CharBlock(required=False, help_text=_("Add designation"))
    
    class Meta:
        icon = "doc-full"
        label = _("Text block with cards")
        
class TopManagementListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    points = blocks.ListBlock(ProfileCardBlock(),label="Add profile cards", help_text="Add profile cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Top Management List Block")

class ManagementListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    points = blocks.ListBlock(ProfileCardBlock(),label="Add profile cards", help_text="Add profile cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Management List Block")
        
        
class ReviewCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    video_source = blocks.ChoiceBlock(
        choices=[
            ('upload', 'Upload Video'),
            ('external', 'External Video Link'),
        ],
        label="Video Source",
        help_text="Choose whether to upload a video or provide an external link."
    )
    uploaded_video = DocumentChooserBlock(
        required=False,
        label="Upload Video",
        help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
    )
    external_video_link = blocks.URLBlock(
        required=False,
        label="External Video Link",
        help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
    )     
    # watch_time = blocks.IntegerBlock(
    #     label="Watch Time (minutes)",
    #     help_text="Estimated time to watch/read the content.",
    #     required=False
    # )        
    thumbnail = ImageChooserBlock(
        label="Thumbnail Image",
        help_text="Choose a thumbnail image for the video."
    )
    name = blocks.CharBlock(required=False, help_text=_("Add name"))
    description = blocks.CharBlock(required=False, help_text=_("Add your description"))
    review = blocks.CharBlock(required=False, help_text=_("Add your review"))
    rating = blocks.DecimalBlock(max_value = 5, decimal_part=1,null=True, blank=True, help_text=_("Add Rating"))
        
    class Meta:
        icon = "media"
        label = "Review Card Block"
    
    def clean(self, value):
        cleaned_data = super().clean(value)
        video_source = cleaned_data.get('video_source')
        uploaded_video = cleaned_data.get('uploaded_video')
        external_video_link = cleaned_data.get('external_video_link')

        if video_source == 'upload':
            if not uploaded_video:
                raise ValidationError({'uploaded_video': 'Please upload a video file.'})
            else:
                # Check if the uploaded file is a video
                allowed_extensions = ['mp4', 'mov', 'avi', 'webm']
                file_extension = uploaded_video.file_extension.lower().lstrip('.')
                if file_extension not in allowed_extensions:
                    raise ValidationError({'uploaded_video': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'})
        elif video_source == 'external' and not external_video_link:
            raise ValidationError({'external_video_link': 'Please provide an external video link.'})

        
        # Prevent both internal and external links from being filled
        if video_source == 'upload' and external_video_link:
            raise ValidationError(_('An external URL should not be provided when video source is upload.'))
        if video_source == 'external' and uploaded_video:
            raise ValidationError(_('An video should not be provided when video source is external.'))

        return cleaned_data    
        
        
class BaseImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    image = ImageChooserBlock(required=True)
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    
    class Meta:
        icon = "media"
        label = "Base Image Block"
           
class NormalTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    points = blocks.ListBlock(TextCardBlock(),label="Add text cards", help_text="Add text cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Normal Image Block")
        
class FeaturesListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    points = blocks.ListBlock(ImageCardBlock(),label="Add image cards", help_text="Add image cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Feature List Block")


class PointTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class Meta:
        icon = "doc-full"
        label = _("Point Text Block")
        
class WhyUsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading")) 
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    points = blocks.ListBlock(ImageCardBlock(),label="Add image cards", help_text="Add image cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    class Meta:
        icon = "doc-full"
        label = _("Why Us Block")



# class AwardsListBlock(blocks.StructBlock):

class OverviewBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    
    class Meta:
        icon = "doc-full"
        label = _("Overview Block")
        
class InfoCardBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading")) 
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,
        max_num=2,
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    ) 
    
    class Meta:
        icon = "doc-full"
        label = _("Info Card Block")
        
class ContactInfoBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading")) 
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading")) 
    points = blocks.ListBlock(InfoCardBlock(),label="Add info cards", help_text="Add info cards to this section")
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
    class Meta:
        icon = "doc-full"
        label = _("Why Us Block")


class SocialSharingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    alignment = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="center", help_text=_("Block Alignment"))
    social_media = blocks.MultipleChoiceBlock(
        choices=SOCIAL_MEDIA_CHOICES,
        help_text=_("Select the social media platforms you want to display."),
        widget=CheckboxSelectMultiple,  # Use checkboxes for the multiple choices
    )


    class Meta:
        icon = "link-external"
        label = _("Social Sharing Block")


class VideoListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    video_source = blocks.ChoiceBlock(
        choices=[
            ('upload', 'Upload Video'),
            ('external', 'External Video Link'),
        ],
        label="Video Source",
        help_text="Choose whether to upload a video or provide an external link."
    )

    uploaded_video = DocumentChooserBlock(
        required=False,
        label="Upload Video",
        help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
    )
    external_video_link = blocks.URLBlock(
        required=False,
        label="External Video Link",
        help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
    )

    thumbnail = ImageChooserBlock(
        label="Thumbnail Image",
        help_text="Choose a thumbnail image for the video."
    )

    link_label = blocks.CharBlock(
        label="Link Label",
        max_length=50,
        help_text="The text for the link button.",
        required=False
    )

    class Meta:
        icon = "media"
        label = _("Video Block")

    def clean(self, value):
        cleaned_data = super().clean(value)
        video_source = cleaned_data.get('video_source')
        uploaded_video = cleaned_data.get('uploaded_video')
        external_video_link = cleaned_data.get('external_video_link')

        if video_source == 'upload':
            if not uploaded_video:
                raise ValidationError({'uploaded_video': 'Please upload a video file.'})
            else:
                # Check if the uploaded file is a video
                allowed_extensions = ['mp4', 'mov', 'avi', 'webm']
                file_extension = uploaded_video.file_extension.lower().lstrip('.')
                if file_extension not in allowed_extensions:
                    raise ValidationError({'uploaded_video': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'})
        elif video_source == 'external' and not external_video_link:
            raise ValidationError({'external_video_link': 'Please provide an external video link.'})

        
        # Prevent both internal and external links from being filled
        if video_source == 'upload' and external_video_link:
            raise ValidationError(_('An external URL should not be provided when video source is upload.'))
        if video_source == 'external' and uploaded_video:
            raise ValidationError(_('An video should not be provided when video source is external.'))

        return cleaned_data
# ----------------------------------- ----------------------------------- ----------------------------------- -----------------------------------     

class RelatedNewsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=BLOG_TARGETS), label="Select related news pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Related News Block")
        
class ProjectListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=BLOG_TARGETS), label="Select project pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Project List Block")
        
class AgentListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=BLOG_TARGETS), label="Select agent pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Agent List Block")
        

class PropertyListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=BLOG_TARGETS), label="Select property pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Property List Block")
        
class DeveloperListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=DEVELOPER_TARGETS), label="Select developer pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Agent List Block")
              
              
class AmenitiesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))  
    links = blocks.ListBlock(
        LinkBlock(),
        min_num=0,  # No minimum requirement
        max_num=2,  # Maximum of two links
        help_text=_("Add button/link information to this section"),
        label="Add link details"
    )
    
    pages = blocks.ListBlock(blocks.PageChooserBlock(page_type=BLOG_TARGETS), label="Select amenities pages")
    
        
    class meta:
        icon = "doc-full"
        label = _("Amenities List Block")
    
    
class FullVideoBlock(blocks.StructBlock):
    video_source = blocks.ChoiceBlock(
        choices=[
            ('upload', 'Upload Video'),
            ('external', 'External Video Link'),
        ],
        label="Video Source",
        help_text="Choose whether to upload a video or provide an external link."
    )
    uploaded_video = DocumentChooserBlock(
        required=False,
        label="Upload Video",
        help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
    )
    external_video_link = blocks.URLBlock(
        required=False,
        label="External Video Link",
        help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
    )
    thumbnail = ImageChooserBlock(
        label="Thumbnail Image",
        help_text="Choose a thumbnail image for the video."
    )
    link_label = blocks.CharBlock(
        label="Link Label",
        max_length=50,
        help_text="The text for the link button.",
        required=False
    )
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
        
    class meta:
        icon = "media"
        label = _("Full Video Block")

    def clean(self, value):
        cleaned_data = super().clean(value)
        video_source = cleaned_data.get('video_source')
        uploaded_video = cleaned_data.get('uploaded_video')
        external_video_link = cleaned_data.get('external_video_link')

        if video_source == 'upload':
            if not uploaded_video:
                raise ValidationError({'uploaded_video': 'Please upload a video file.'})
            else:
                # Check if the uploaded file is a video
                allowed_extensions = ['mp4', 'mov', 'avi', 'webm']
                file_extension = uploaded_video.file_extension.lower().lstrip('.')
                if file_extension not in allowed_extensions:
                    raise ValidationError({'uploaded_video': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'})
        elif video_source == 'external' and not external_video_link:
            raise ValidationError({'external_video_link': 'Please provide an external video link.'})

        
        # Prevent both internal and external links from being filled
        if video_source == 'upload' and external_video_link:
            raise ValidationError(_('An external URL should not be provided when video source is upload.'))
        if video_source == 'external' and uploaded_video:
            raise ValidationError(_('An video should not be provided when video source is external.'))

        return cleaned_data
    
class FullImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
        
    class meta:
        icon = "media"
        label = _("Full Video Block")
        
class MultiContentOverlayedBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    main_image = ImageChooserBlock(required=True)    
    secondary_image = ImageChooserBlock(required=True) 
    points = blocks.ListBlock(BaseContentBlock(),label="Add content", help_text="Add multiple content to this section") 
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    image_alignment = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="center", help_text=_("Block Alignment"))
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
    
    class Meta:
        icon = "image"
        label = _("Multi Content Overlayed Image Block")
    
class MultiContentImageBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    image = ImageChooserBlock(required=False)
    points = blocks.ListBlock(BaseContentBlock(),label="Add content", help_text="Add multiple content to this section") 
    background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
    top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
    bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
    image_alignment = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="center", help_text=_("Block Alignment"))
    component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))

    class meta:
        icon = "image"
        label = _("Multi Content Image Block")



# -----------------------------------------------------------------------------------------------------------------------------
# # project listing block
# class ProjectBlock(blocks.StructBlock):
#     developer = blocks.CharBlock(required=False, help_text=_("Add developer"))
#     points = blocks.ListBlock(ProjectDetailBlock(), label="Add points", help_text="Add multiple points to this section")
#     heading = blocks.CharBlock(required=False, help_text=_("Add project"))
#     sub_heading = blocks.CharBlock(required=False, help_text=_("Add detail"))
#     images = blocks.ListBlock(ImageBlock(), label="Add images", help_text="Add multiple images to this section")     
#     class meta:
#         icon = "doc-full"
#         label = _("Project Block")
        
# class AmenitiesListBlock(blocks.StructBlock):
#     icon = ImageChooserBlock(required=False) 
#     description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add description"))
#     class meta:
#         icon = "doc-full"
#         label = _("Amenities List Block")
    
# class AmentiesBlock(blocks.StructBlock):
#     heading = blocks.CharBlock(required=False, help_text=_("Add heading"))
#     points = blocks.ListBlock(AmenitiesListBlock(), label = "Add details", help_text="add multiple amenities here")
    
#     class meta:
#         icon = "doc-full"
#         label = _("Amenities Block")
    
# class MultiDetailBlock(blocks.StructBlock):
#     image = ImageChooserBlock(required=False) 
#     heading = blocks.CharBlock(required=False, help_text=_("Add heading"))
#     description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add description"))    
#     class meta:
#         icon = "doc-full"
#         label = _("Multidata Block")
        
       
# class ServiceBlock(blocks.StructBlock):
#     heading = blocks.CharBlock(required=False, help_text=_("Add heading"))
#     sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
#     description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add description"))    
#     points = blocks.ListBlock(MultiDetailBlock(),label="Add services", help_text=_("Add services"))
#     class meta:
#         icon = "doc-full"
#         label = _("Service Block")
 
    
# class DeveloperBlock(blocks.StructBlock):
#     heading = blocks.CharBlock(required=False, help_text=_("Add heading"))
#     sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
#     description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add description")) 
#     image = ImageChooserBlock(required=False)
#     project = blocks.CharBlock(required=False, help_text=_("Add project count"))
#     founded_in = blocks.CharBlock(required=False, help_text=_("Add founded year"))
#     price_from = blocks.CharBlock(required=False, help_text=_("Add price starts from"))
#     background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
#     top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
#     bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
#     component_type = blocks.ChoiceBlock(max_length=20, choices=COMPONENT_TYPE,  null=True, blank=True, default="all", help_text=_("Component Type"))
        
#     class meta:
#         icon = "doc-full"
#         label = _("Developer Block")

# -----------------------------------------------------------------------------------------------------------------------------