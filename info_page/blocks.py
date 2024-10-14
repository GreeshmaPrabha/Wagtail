from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError
from mysite.constantvariables import *

class BaseHeadingBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True, help_text=_("Add your heading"))
    
    class Meta:
        icon = "doc-full"
        label = "Base Heading Block"
        
class PartnerPageListBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class Meta:
        icon = "doc-full"
        label = "Partner Page List Block"

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context['preview'] = f"""
            <div class="block-preview">
                <h2>{value.get('heading')}</h2>
                <h3>{value.get('sub_heading', '')}</h3>
                <p>{value.get('description', '')}</p>
            </div>
        """
        return context

#base text block with heading and description
class BaseTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=True, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))

    class Meta:
        icon = "doc-full"
        label = "Base Text Block"

# base text block with image  
class AboutUsBlock(BaseTextBlock):
    image = ImageChooserBlock(required=True)
    class Meta:
        icon = "doc-full"
        label = "About us Block"
        
class TeamListBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    name = blocks.CharBlock(required=True, help_text=_("Add your name"))
    designation = blocks.CharBlock(required=True, help_text=_("Add your designation"))
    
    class Meta:
        icon = "doc-full"
        label = "Team Block"

# team list block with an additional description   
class TeamDescriptionBlock(TeamListBlock):
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))

    class Meta:
        icon = "doc-full"
        label = "Team Block with description"
        

class AgentListBlock(TeamListBlock):
    whatsapp_no = blocks.CharBlock(required=True, help_text=_("Add your whatsapp number"))
    mobile_no = blocks.CharBlock(required=True, help_text=_("Add your contact number"))
    email = blocks.EmailBlock(required=False, help_text=_("Add your email"))
    
    class meta:
        icon = "doc-full"
        label = "Team Block with contact details"
    
    
class ValueListBlock(BaseTextBlock):
    icon = ImageChooserBlock(required=True)
    
    class Meta:
        icon = "doc-full"
        label = "Value list Block"
    
    
class AgentDescriptionBlock(blocks.StructBlock):
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class Meta:
        icon = "doc-full"
        label = "Team Block with description"
        
class ContactBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    heading = blocks.CharBlock(required=True, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    whatsapp_no = blocks.CharBlock(required=True, help_text=_("Add your whatsapp number"))
    mobile_no = blocks.CharBlock(required=True, help_text=_("Add your contact number"))
    
    class meta:
        icon = "doc-full"
        label = "Contact Block"

class PodcastPointblock(blocks.StructBlock):
    points = blocks.CharBlock(required=False, help_text=_("Add your points"))
    
    class meta:
        icon = "doc-full"
        label = "Point Block"
                
class PodcastBlock(blocks.StructBlock):
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
        required=True
    )        
    thumbnail = ImageChooserBlock(
        label="Thumbnail Image",
        help_text="Choose a thumbnail image for the video."
    )
    date = blocks.CharBlock(required=False, help_text=_("Add date"))
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    points = blocks.ListBlock(PodcastPointblock(), label="Add text card", help_text="Add multiple points to this section")
    
    class Meta:
        icon = "media"
        label = "Podcast Block"
        
class CareerContentBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    sub_heading = blocks.CharBlock(required=False, help_text=_("Add your sub heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    
    class meta:
        icon = "doc-full"
        label = "Career Content Block"
        
        
class MoreContentBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    description = blocks.RichTextBlock(editor='default',required=False, help_text=_("Add additional text"))
    image = ImageChooserBlock(required=False)
    industried = blocks.ListBlock(PodcastPointblock(), label="Add industries", help_text="Add multiple points to this section")
        
    class meta:
        icon = "doc-full"
        label = "Report Content Block"
        
class MultiplePageChooserBlock(blocks.StructBlock):
    page = blocks.PageChooserBlock(required=False)  
    class meta:
        icon = "doc-full"
        label = "Related News Page Block"   
       
class RelatedNewsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False, help_text=_("Add your heading"))
    related_news = blocks.ListBlock(MultiplePageChooserBlock(), label="Add pages", help_text="Add related news to this section")
        
    class meta:
        icon = "doc-full"
        label = "Related News Block"
        
