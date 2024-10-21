# from wagtail import blocks
# from wagtail.images.blocks import ImageChooserBlock
# from django.utils.translation import gettext_lazy as _
# from django.core.exceptions import ValidationError
# from mysite.constantvariables import *
# from wagtail.documents.blocks import DocumentChooserBlock
# from .blocks import *


# class BaseContentBlock(blocks.StructBlock):
#     heading = blocks.CharBlock(required=False, max_length=250)
#     content = blocks.RichTextBlock(required=False)  
#     image = ImageChooserBlock(required=False)



# class LinkBlock(blocks.StructBlock):
#     """
#     A block that allows users to create links, either to an internal page or an external URL.
#     Validates that only one of internal or external links is provided, and ensures required fields are filled
#     based on the selected link type.
#     """
#     label = blocks.CharBlock(required=False, help_text=_("Enter the label of the link"))  # Link text
#     link_type = blocks.ChoiceBlock(
#         choices=[
#             ('internal', _('Internal Page')),
#             ('external', _('External URL')),
#         ],
#         default='internal',
#         help_text=_("Select the type of link"),
#     )  
#     internal_page = blocks.PageChooserBlock(
#         required = False, 
#         help_text = _("Select an internal page"),
#         # target_model = PAGE_TARGETS
#     )  
#     external_url = blocks.URLBlock(
#         required=False, 
#         help_text=_("Enter an external URL"),
#     ) 

#     def clean(self, value):
#         """
#         Custom validation to ensure that only one type of link (internal or external) is provided,
#         and that the appropriate fields are filled based on the selected link type.
#         """
#         cleaned_data = super().clean(value)
#         link_type = cleaned_data.get('link_type')
#         internal_page = cleaned_data.get('internal_page')
#         external_url = cleaned_data.get('external_url')


#         if link_type == 'internal' and not internal_page:
#             raise ValidationError(_('An internal page must be selected when "Internal Page" is chosen.'))
#         elif link_type == 'external' and not external_url:
#             raise ValidationError(_('A URL must be provided when "External URL" is chosen.'))

#         if link_type == 'internal' and external_url:
#             raise ValidationError(_('An external URL should not be provided when linking to an internal page.'))
#         if link_type == 'external' and internal_page:
#             raise ValidationError(_('An internal page should not be provided when linking to an external URL.'))

#         return cleaned_data

#     class Meta:
#         label = _("Link Information")
#         icon = 'link'
        
        
        
# class CareerBlock(blocks.StructBlock):
#     """
#     A block used to represent a career section, including a heading, location, posted time, image, and a links.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading")) 
#     location = blocks.CharBlock(required=False, help_text=_("Add your location"))
#     time = blocks.CharBlock(required=False, help_text=_("Posted time"))
#     image = ImageChooserBlock(required=False) 
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  # Minimum number of links is zero (optional)
#     #     max_num=1,  # Maximum number of links is one
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # )  # Allow up to two links (either internal or external)

#     class Meta:
#         icon = "doc-full"
#         label = _("Career Block")
        
        
# class AwardListBlock(blocks.StructBlock):
#     """
#     A block used to represent a events and award section, including a image, and a descriptions.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
#     sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
#     points = blocks.ListBlock(ImageCardBlock(),label="Add image cards", help_text="Add image cards to this section")
#     background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
#     top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
#     bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
#     component_type = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="all", help_text=_("Component Type"))
#     card_count = blocks.ChoiceBlock(max_length=20, choices=CARD_CHOICES,  null=True, blank=True, default="3", help_text=_("Number of cards"))
    
#     class Meta:
#         icon = "doc-full"
#         label = _("Award List Block")
        
        

# class MarketTrendsBlock(blocks.StructBlock):
#     """
#     A block used to represent a events and award section, including a image, and a descriptions.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     image = ImageChooserBlock(required=False) 
#     description  = blocks.RichTextBlock(editor='default', required=False, help_text=_("Add additional text"))
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("MarketTrends Block")
        
# class VideoCardBlock(blocks.StructBlock):
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
#     video_source = blocks.ChoiceBlock(
#         choices=[
#             ('upload', 'Upload Video'),
#             ('external', 'External Video Link'),
#         ],
#         label="Video Source",
#         help_text="Choose whether to upload a video or provide an external link."
#     )

#     uploaded_video = DocumentChooserBlock(
#         required=False,
#         label="Upload Video",
#         help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
#     )
#     external_video_link = blocks.URLBlock(
#         required=False,
#         label="External Video Link",
#         help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
#     )   

#     watch_time = blocks.IntegerBlock(
#         label="Watch Time (minutes)",
#         help_text="Estimated time to watch/read the content.",
#         required=False
#     )

#     proficiency_level = blocks.ChoiceBlock(
#         choices=PROFICIENCY_LEVEL_CHOICES,
#         label="Proficiency Level",
#         help_text="Select the difficulty level."
#     )

#     thumbnail = ImageChooserBlock(
#         label="Thumbnail Image",
#         help_text="Choose a thumbnail image for the video."
#     )

#     link_label = blocks.CharBlock(
#         label="Link Label",
#         max_length=50,
#         help_text="The text for the link button.",
#         required=False
#     )

#     class Meta:
#         icon = "media"
#         label = "Video Block"

#     def clean(self, value):
#         cleaned_data = super().clean(value)
#         video_source = cleaned_data.get('video_source')
#         uploaded_video = cleaned_data.get('uploaded_video')
#         external_video_link = cleaned_data.get('external_video_link')

#         if video_source == 'upload':
#             if not uploaded_video:
#                 raise ValidationError({'uploaded_video': 'Please upload a video file.'})
#             else:
#                 # Check if the uploaded file is a video
#                 allowed_extensions = ['mp4', 'mov', 'avi', 'webm']
#                 file_extension = uploaded_video.file_extension.lower().lstrip('.')
#                 if file_extension not in allowed_extensions:
#                     raise ValidationError({'uploaded_video': f'Invalid file type. Allowed types are: {", ".join(allowed_extensions)}'})
#         elif video_source == 'external' and not external_video_link:
#             raise ValidationError({'external_video_link': 'Please provide an external video link.'})

#         # Prevent both internal and external links from being filled
#         if video_source == 'upload' and external_video_link:
#             raise ValidationError(_('An external URL should not be provided when video source is upload.'))
#         if video_source == 'external' and uploaded_video:
#             raise ValidationError(_('An video should not be provided when video source is external.'))

#         return cleaned_data
    
      
# class PodcastBlogBlock(blocks.StructBlock):
#     """
#     A block used to represent a podcast section, including a video, posted date and a descriptions.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     # video = blocks.ListBlock(VideoCardBlock(), label="Add text card", help_text="Add multiple video cards to this section")
#     video_source = blocks.ChoiceBlock(
#         choices=[
#             ('upload', 'Upload Video'),
#             ('external', 'External Video Link'),
#         ],
#         label="Video Source",
#         help_text="Choose whether to upload a video or provide an external link."
#     )

#     uploaded_video = DocumentChooserBlock(
#         required=False,
#         label="Upload Video",
#         help_text="Upload a video file (MP4, MOV, AVI, or WebM)",
#     )
#     external_video_link = blocks.URLBlock(
#         required=False,
#         label="External Video Link",
#         help_text="Paste the URL of an external video (e.g., YouTube, Vimeo)",
#     )   

#     watch_time = blocks.IntegerBlock(
#         label="Watch Time (minutes)",
#         help_text="Estimated time to watch/read the content.",
#         required=False
#     )

#     proficiency_level = blocks.ChoiceBlock(
#         choices=PROFICIENCY_LEVEL_CHOICES,
#         label="Proficiency Level",
#         help_text="Select the difficulty level."
#     )

#     thumbnail = ImageChooserBlock(
#         label="Thumbnail Image",
#         help_text="Choose a thumbnail image for the video."
#     )

#     link_label = blocks.CharBlock(
#         label="Link Label",
#         max_length=50,
#         help_text="The text for the link button.",
#         required=False
#     )
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading")) 
#     description  = blocks.RichTextBlock(editor='default', required=False, help_text=_("Add additional text"))
#     posted_date = blocks.CharBlock(required=False, help_text=_("Posted date"))
#     is_featured = blocks.BooleanBlock(required=False, help_text="Check this box to show as featured.")
#     background = blocks.ChoiceBlock(max_length=50, choices=BG_CHOICES,  null=True, blank=True, default="transparent", help_text=_("Block Backgound"))
#     top_padding = blocks.ChoiceBlock(max_length=50, choices=TOP_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Top padding"))
#     bottom_padding = blocks.ChoiceBlock(max_length=50, choices=BOTTOM_PADDING_CHOICES,  null=True, blank=True, default="big", help_text=_("Bottom padding"))      
#     component_type = blocks.ChoiceBlock(max_length=20, choices=ALIGNMENT_CHOICES,  null=True, blank=True, default="all", help_text=_("Component Type"))
     

#     class Meta:
#         icon = "site"
#         label = _("Podcast Block")
        
  
        
# class ReportsBlock(blocks.StructBlock):
#     """
#     A block used to represent a report section, including a image, date and a descriptions.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     image = ImageChooserBlock(required=False)
#     posted_date = blocks.CharBlock(required=False, help_text=_("Posted date"))
#     description  = blocks.RichTextBlock(editor='default', required=False, help_text=_("Add additional text"))
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("Reports Block")
        
# class NewsContentBlock(blocks.StructBlock):
#     """
#     A block used to represent a news section, including a image, date and a descriptions.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     image = ImageChooserBlock(required=False)
#     posted_date = blocks.CharBlock(required=False, help_text=_("Posted date"))
#     description  = blocks.RichTextBlock(editor='default', required=False, help_text=_("Add additional text"))
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("News Content Block")
        
# class NewsBlock(blocks.StructBlock):
#     """
#     A block used to represent a news section, including a heading and content.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))   
#     content = blocks.ListBlock(NewsContentBlock(), label="Add text card", help_text="Add multiple news to this section") 
    
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("News Block")
        
# class MediaBlock(blocks.StructBlock):
#     """
#     A block used to represent a media section, including a heading and content.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))   
#     content = blocks.ListBlock(NewsContentBlock(), label="Add text card", help_text="Add multiple news to this section") 
    
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("Media Block")
        
# class NewsletterBlock(blocks.StructBlock):
#     """
#     A block used to represent a newsletter section, including a heading and content.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))   
#     content = blocks.ListBlock(NewsContentBlock(), label="Add text card", help_text="Add multiple news to this section") 
    
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("NewsLetter Block")
        
# class BlogBlock(blocks.StructBlock):
#     """
#     A block used to represent a blog section, including a heading and content.
#     It allows users to add an image along with text and optional links that can be either internal or external.
#     """
#     heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))   
#     content = blocks.ListBlock(NewsContentBlock(), label="Add text card", help_text="Add multiple news to this section") 
    
#     # links = blocks.ListBlock(
#     #     LinkBlock(),
#     #     min_num=0,  
#     #     max_num=1,  
#     #     help_text=_("Add button/link information to this section"),
#     #     label="Add link details"
#     # ) 

#     class Meta:
#         icon = "site"
#         label = _("Blog Block")