from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from bs4 import BeautifulSoup
from wagtail.rich_text import RichText
from wagtail.models import Page
from wagtail.images.models import Image
from django.conf import settings
from django.db.models import F
from mysite.constantvariables import *
from .utils import get_image_rendition

class BannerFieldsSerializer(serializers.Serializer):
    banner_heading = serializers.CharField(read_only=True)
    banner_subheading = serializers.CharField(read_only=True)
    banner_description = serializers.CharField(read_only=True)
    banner_header_image = serializers.SerializerMethodField(read_only=True)

    def get_banner_header_image(self, obj):
        if obj.banner_header_image:
            image = obj.banner_header_image
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
class SEOFieldsSerializer(serializers.Serializer):
    seo_title = serializers.CharField(read_only=True)
    seo_description = serializers.CharField(read_only=True, source="search_description")
    seo_type = serializers.CharField(read_only=True)
    # seo_description = serializers.CharField(read_only=True)
    seo_keywords = serializers.CharField(read_only=True)
    canonical_url = serializers.CharField(read_only=True)
    og_title = serializers.CharField(read_only=True)
    og_description = serializers.CharField(read_only=True)
    og_image = ImageRenditionField('fill-800x450')  # Example rendition


# -----------------------------------------------------------------------
class OverlayedImageBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    main_image = serializers.SerializerMethodField(read_only=True)
    secondary_image = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    alignment = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
    def get_main_image(self, obj):
        if obj.get('main_image'):
            image = obj['main_image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_secondary_image(self, obj):
        if obj.get('secondary_image'):
            image = obj['secondary_image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
 
 
class BaseContentBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    

class ImageCardSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None

class NormalImageBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    points = ImageCardSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    card_count = serializers.CharField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    

# ------------------------------------------------------------   
class BaseTextBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
class AboutUsBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
class TeamListBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
class TeamDescriptionBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)    
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None

class AgentListBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)    
    whatsapp_no = serializers.CharField()
    mobile_no = serializers.CharField()
    email = serializers.CharField()
    
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
  
class ValueListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    icon = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)
    
    def get_icon(self, obj):
        if obj.get('icon'):
            image = obj['icon']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
 
class AgentDescriptionBlockSerializer(serializers.Serializer):
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)    

class ContactBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    whatsapp_no = serializers.CharField(read_only=True)
    mobile_no = serializers.CharField(read_only=True)
    
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)    


class PodcastPointBlockSerializer(serializers.Serializer):
    points = serializers.CharField(read_only=True)
    
class PodcastBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    video_source = serializers.CharField(read_only=True)
    upload_video = serializers.SerializerMethodField(read_only=True)
    external_video_link = serializers.URLField(read_only=True)
    watch_time = serializers.IntegerField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    date = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    # points = serializers.SerializerMethodField(read_only=True)
    points = serializers.ListField(child=PodcastPointBlockSerializer())
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)  
    
    def get_thumbnail(self, obj):
        if obj.get('thumbnail'):
            image = obj['thumbnail']
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_upload_video(self, obj):
        # Assuming `uploaded_video` is a field in the StreamField
        uploaded_video = obj.get('uploaded_video')  # Access the DocumentChooserBlock
        
        if uploaded_video:  # Check if a video is uploaded
            return settings.BASE_URL + uploaded_video.url  # Return the URL of the uploaded video
        return None  # Return None if no video is uploaded
    
class BaseHeadingBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    
class CareerBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    location = serializers.CharField(read_only=True)
    time = serializers.CharField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
class EventsAwardsBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)    
    
class TextBlockSerializer(serializers.Serializer):
    heading =  serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content  # or raise an exception if request is required

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)    
 
class MarketTrendsBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content 

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)    
       

class VideoBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    video_source = serializers.CharField(read_only=True)
    upload_video = serializers.SerializerMethodField(read_only=True)
    external_video_link = serializers.URLField(read_only=True)
    watch_time = serializers.IntegerField(read_only=True)
    proficiency_level = serializers.SerializerMethodField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    link_label = serializers.CharField(read_only=True)

    def get_thumbnail(self, obj):
        if obj.get('thumbnail'):
            image = obj['thumbnail']
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_upload_video(self, obj):
        # Assuming `uploaded_video` is a field in the StreamField
        uploaded_video = obj.get('uploaded_video')  # Access the DocumentChooserBlock
        
        if uploaded_video:  # Check if a video is uploaded
            return settings.BASE_URL + uploaded_video.url  # Return the URL of the uploaded video
        return None  # Return None if no video is uploaded
    
    def get_proficiency_level(self, obj):
        """
        Fetch the display name of the proficiency level.
        """
        proficiency_level_value = obj.get('proficiency_level')

        # Loop through the choices and find the label for the value
        for choice_value, choice_label in PROFICIENCY_LEVEL_CHOICES:
            if choice_value == proficiency_level_value:
                return choice_label  # Return the display label
        
        return proficiency_level_value  # Return the value if no match is found

class ReportBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    posted_date = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content 

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)


class NewsContentBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    posted_date = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    
    def get_image(self, obj):
        if obj.get('image'):
            image = obj['image']
            
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None
    
    def get_description(self, instance):
        content = instance.get('description')
        if not content:
            return None

        # Ensure content is a string
        if isinstance(content, RichText):
            content = str(content)

        request = self.context.get('request')
        if not request:
            return content 

        soup = BeautifulSoup(content, 'html.parser')
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src')
            if src:
                img_tag['src'] = request.build_absolute_uri(src)

        return str(soup)


class NewsBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    content = serializers.ListField(child=NewsContentBlockSerializer())
   
   
class MediaBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    content = serializers.ListField(child=NewsContentBlockSerializer())
  
class PageContentMixin:
    def get_content(self, obj):
        content_blocks = []
        request = self.context.get('request')
        for block in obj.content:
            if block.block_type == 'overlayed_image_block':
                content_blocks.append({
                    'type': 'overlayed_image_block',
                    'value': OverlayedImageBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'base_content_block':
                content_blocks.append({
                    'type': 'base_content_block',
                    'value': BaseContentBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'about_us_block':
                content_blocks.append({
                    'type': 'about_us_block',
                    'value': AboutUsBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'team_list_block':
                content_blocks.append({
                    'type': 'team_list_block',
                    'value': TeamListBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'team_description_block':
                content_blocks.append({
                    'type': 'team_description_block',
                    'value': TeamDescriptionBlockSerializer(block.value, context={'parent': self}).data
                })                
            elif block.block_type == 'agent_list_block':
                content_blocks.append({
                    'type': 'agent_list_block',
                    'value': AgentListBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'value_list_block':
                content_blocks.append({
                    'type': 'value_list_block',
                    'value': ValueListBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'agent_description_block':
                content_blocks.append({
                    'type': 'agent_description_block',
                    'value': AgentDescriptionBlockSerializer(block.value, context={'parent': self}).data
                })  
            elif block.block_type == 'contact_block':
                content_blocks.append({
                    'type': 'contact_block',
                    'value': ContactBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'podcast_block':
                content_blocks.append({
                    'type': 'podcast_block',
                    'value': PodcastBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'base_heading_block':
                content_blocks.append({
                    'type': 'base_heading_block',
                    'value': BaseHeadingBlockSerializer(block.value, context={'parent': self}).data
                })      
            # elif block.block_type == 'link_block':
            #     content_blocks.append({
            #         'type': 'link_block',
            #         'value': LinkBlockSerializer(block.value, context={'parent': self}).data
            #     })   
            elif block.block_type == 'career_block':
                content_blocks.append({
                    'type': 'career_block',
                    'value': CareerBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'event_awards_block':
                content_blocks.append({
                    'type': 'event_awards_block',
                    'value': EventsAwardsBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'text_block':
                content_blocks.append({
                    'type': 'text_block',
                    'value': TextBlockSerializer(block.value, context={'parent': self,'request': request}).data
                })     
            elif block.block_type == 'market_trend_block':
                content_blocks.append({
                    'type': 'market_trend_block',
                    'value': MarketTrendsBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'video_block':
                content_blocks.append({
                    'type': 'video_block',
                    'value': VideoBlockSerializer(block.value, context={'parent': self}).data
                })                
            elif block.block_type == 'podcast_block':
                content_blocks.append({
                    'type': 'podcast_block',
                    'value': PodcastBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'report_block':
                content_blocks.append({
                    'type': 'report_block',
                    'value': ReportBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'news_block':
                content_blocks.append({
                    'type': 'news_block',
                    'value': NewsBlockSerializer(block.value, context={'parent': self}).data
                })  
            elif block.block_type == 'media_block':
                content_blocks.append({
                    'type': 'media_block',
                    'value': MediaBlockSerializer(block.value, context={'parent': self}).data
                })  
            
        return content_blocks