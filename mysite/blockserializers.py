from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from bs4 import BeautifulSoup
from wagtail.rich_text import RichText
from wagtail.models import Page
from wagtail.images.models import Image
from django.conf import settings
from django.db.models import F
from mysite.constantvariables import *
from .utils import get_image_rendition,local_timezone
from info_page.models import BlogLinkPage

def get_frontend_folder(key):
    for item in FRONTEND_FOLDERS:
        if item[0] == key:
            return item[1]
    return None 
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

class PageSerializer(serializers.ModelSerializer):
    page_type = serializers.SerializerMethodField()
    class Meta:
        model = Page
        fields = ['slug','page_type']
    
    def get_page_type(self, obj):
        return obj.specific._meta.model_name

class LinkBlockSerializer(serializers.Serializer):
    label = serializers.CharField(read_only=True)
    link_type = serializers.CharField(read_only=True)
    internal_page = PageSerializer(required=False)
    external_url = serializers.URLField(required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.get('internal_page'):
            if isinstance(instance['internal_page'], Page):
                # If it's already a Page object, just serialize it
                data['internal_page'] = PageSerializer(instance['internal_page']).data
            else:
                # If it's an ID, fetch the Page object first
                try:
                    page = Page.objects.get(id=instance['internal_page'])
                    data['internal_page'] = PageSerializer(page).data
                except Page.DoesNotExist:
                    data['internal_page'] = None
        return data

class BaseFaqBlockSerializer(serializers.Serializer):
    question = serializers.CharField(read_only=True)
    answer = serializers.SerializerMethodField(read_only=True)
    def get_answer(self, instance):
        content = instance.get('answer')
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
    
class FAQBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    full_width = serializers.BooleanField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)    
    tab_name = serializers.CharField(read_only=True)
    tab_key = serializers.CharField(read_only=True)
    points = serializers.ListField(child=BaseFaqBlockSerializer())

    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
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
    image_alignment = serializers.CharField(read_only=True)
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


class ImageBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    image_alignment = serializers.CharField(read_only=True)
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
    
    def get_image(self, obj):
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
    
    
class TextCardBlockSerializer(serializers.Serializer):
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
    
class ManagementMessageBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    designation = serializers.CharField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    
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
    
    def get_message(self, instance):
        content = instance.get('message')
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
    
    
class ProfileCardBlockSerializer(serializers.Serializer):
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
        

class TopManagementListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    points = ProfileCardBlockSerializer(many=True)
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
    

class ManagementListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    points = ProfileCardBlockSerializer(many=True)
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


class ReviewCardBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    video_source = serializers.CharField(read_only=True)
    upload_video = serializers.SerializerMethodField(read_only=True)
    external_video_link = serializers.URLField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    review = serializers.CharField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    
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
    
 
class BaseImageBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
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

class NormalTextBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    points = TextCardBlockSerializer(many=True)
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
    
class FeaturesListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    points = ImageCardSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    card_count = serializers.CharField(read_only=True)
    
class PointTextBlockSerializer(serializers.Serializer):
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

class WhyUsBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    points = ImageCardSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)

class OverviewBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
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


class InfoCardBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)

    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
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

class ContactInfoBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    points = InfoCardBlockSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)
    card_count = serializers.CharField(read_only=True)



class SocialSharingBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    alignment = serializers.CharField(read_only=True)
    social_media = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )
    

class RelatedNewsBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField() 
    
    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
    def get_pages(self, instance):
        # import pdb; pdb.set_trace()
        pages = instance.get('pages')
        related_news = []
        # request = self.context['request']
        request = self.context['parent'].context['request']
        
        for page in pages:
            # Access the specific instance of the page
            page_specific = page.specific
            reading_time = None
            # Check if the page has an image field
            if hasattr(page_specific, 'banner_image') and page_specific.banner_image:
                image = page_specific.banner_image
                image_data = get_image_rendition(image, 'original')
            else:
                image_data = None  # No image found

            # Check if the page has an first_published_at field
            if hasattr(page_specific, 'date') and page_specific.date:
                date = page_specific.date
            #     date_data = local_timezone(request,date,"%d-%m-%Y")
            # else:
            #     date_data = local_timezone(request,page_specific.date,"%d-%m-%Y")


            if hasattr(page_specific, 'reading_time') and page_specific.reading_time:
                reading_time = page_specific.reading_time
            internal_page_model_name = page_specific._meta.model_name
            page_parent_page = page_specific.get_parent()
            linked_page = BlogLinkPage.objects.filter(internal_page=page_parent_page).first()
            # print(page.get_parent(),"-------------linked_pages-------------------",linked_page.get_parent())
            tab_slug = ''
            parent_slug = ''
            if linked_page:
                tab_slug = linked_page.slug
                parent_slug = linked_page.get_parent().slug
            related_data = {
                'page_id': page.id, #added article id 
                'page_title': page.title, #added article title 
                'slug': page.slug, #added article slug 
                'date':date, #added article first_published_at date 
                'reading_time':reading_time, #added article reading  
                # 'page_type': internal_page_model_name,  #added article model name  
                'folder_name': get_frontend_folder(internal_page_model_name),  #folder name of the model for frontend url
                'tab_slug': parent_slug, #tab slug of the model for frontend url
                'page_slug': tab_slug, #page slug of the model for frontend url
                'image': image_data,                
                }
            related_news.append(related_data)
        return related_news
    
    
class ProjectListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField() 
    
    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
    def get_pages(self, instance):
        pages = instance.get('pages')
        agent_list = []
        request = self.context['request']
        
        for page in pages:
            # Access the specific instance of the page
            page_specific = page.specific
            reading_time = None
            # Check if the page has an image field
            if hasattr(page_specific, 'banner_image') and page_specific.banner_image:
                image = page_specific.banner_image
                image_data = get_image_rendition(image, 'original')
            else:
                image_data = None  # No image found

            # Check if the page has an first_published_at field
            if hasattr(page_specific, 'date') and page_specific.date:
                date = page_specific.date
                date_data = local_timezone(request,date,"%d-%m-%Y")
            else:
                date_data = local_timezone(request,page_specific.date,"%d-%m-%Y")


            if hasattr(page_specific, 'reading_time') and page_specific.reading_time:
                reading_time = page_specific.reading_time
            internal_page_model_name = page_specific._meta.model_name
            page_parent_page = page_specific.get_parent()
            linked_page = BlogLinkPage.objects.filter(internal_page=page_parent_page).first()
            # print(page.get_parent(),"-------------linked_pages-------------------",linked_page.get_parent())
            tab_slug = ''
            parent_slug = ''
            if linked_page:
                tab_slug = linked_page.slug
                parent_slug = linked_page.get_parent().slug
            project_data = {
                'page_id': page.id, #added article id 
                'page_title': page.title, #added article title 
                'slug': page.slug, #added article slug 
                'date':date_data, #added article first_published_at date 
                'reading_time':reading_time, #added article reading  
                # 'page_type': internal_page_model_name,  #added article model name  
                'folder_name': get_frontend_folder(internal_page_model_name),  #folder name of the model for frontend url
                'tab_slug': parent_slug, #tab slug of the model for frontend url
                'page_slug': tab_slug, #page slug of the model for frontend url
                'image': image_data,                
                }
            agent_list.append(project_data)
        return agent_list
    
class AgentListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField() 
    
    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
    def get_pages(self, instance):
        pages = instance.get('pages')
        agent_list = []
        request = self.context['request']
        
        for page in pages:
            # Access the specific instance of the page
            page_specific = page.specific
            reading_time = None
            # Check if the page has an image field
            if hasattr(page_specific, 'banner_image') and page_specific.banner_image:
                image = page_specific.banner_image
                image_data = get_image_rendition(image, 'original')
            else:
                image_data = None  # No image found

            # Check if the page has an first_published_at field
            if hasattr(page_specific, 'date') and page_specific.date:
                date = page_specific.date
                date_data = local_timezone(request,date,"%d-%m-%Y")
            else:
                date_data = local_timezone(request,page_specific.date,"%d-%m-%Y")


            if hasattr(page_specific, 'reading_time') and page_specific.reading_time:
                reading_time = page_specific.reading_time
            internal_page_model_name = page_specific._meta.model_name
            page_parent_page = page_specific.get_parent()
            linked_page = BlogLinkPage.objects.filter(internal_page=page_parent_page).first()
            # print(page.get_parent(),"-------------linked_pages-------------------",linked_page.get_parent())
            tab_slug = ''
            parent_slug = ''
            if linked_page:
                tab_slug = linked_page.slug
                parent_slug = linked_page.get_parent().slug
            agent_data = {
                'page_id': page.id, #added article id 
                'page_title': page.title, #added article title 
                'slug': page.slug, #added article slug 
                'date':date_data, #added article first_published_at date 
                'reading_time':reading_time, #added article reading  
                # 'page_type': internal_page_model_name,  #added article model name  
                'folder_name': get_frontend_folder(internal_page_model_name),  #folder name of the model for frontend url
                'tab_slug': parent_slug, #tab slug of the model for frontend url
                'page_slug': tab_slug, #page slug of the model for frontend url
                'image': image_data,                
                }
            agent_list.append(agent_data)
        return agent_list
    

class DeveloperListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField() 
    
    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
    def get_pages(self, instance):
        pages = instance.get('pages')
        dev_list = []
        request = self.context['request']
        
        for page in pages:
            # Access the specific instance of the page
            page_specific = page.specific
            reading_time = None
            # Check if the page has an image field
            if hasattr(page_specific, 'banner_image') and page_specific.banner_image:
                image = page_specific.banner_image
                image_data = get_image_rendition(image, 'original')
            else:
                image_data = None  # No image found

            # Check if the page has an first_published_at field
            if hasattr(page_specific, 'date') and page_specific.date:
                date = page_specific.date
                date_data = local_timezone(request,date,"%d-%m-%Y")
            else:
                date_data = local_timezone(request,page_specific.date,"%d-%m-%Y")


            if hasattr(page_specific, 'reading_time') and page_specific.reading_time:
                reading_time = page_specific.reading_time
            internal_page_model_name = page_specific._meta.model_name
            page_parent_page = page_specific.get_parent()
            linked_page = BlogLinkPage.objects.filter(internal_page=page_parent_page).first()
            # print(page.get_parent(),"-------------linked_pages-------------------",linked_page.get_parent())
            tab_slug = ''
            parent_slug = ''
            if linked_page:
                tab_slug = linked_page.slug
                parent_slug = linked_page.get_parent().slug
            developer_data = {
                'page_id': page.id, #added article id 
                'page_title': page.title, #added article title 
                'slug': page.slug, #added article slug 
                'date':date_data, #added article first_published_at date 
                'reading_time':reading_time, #added article reading  
                # 'page_type': internal_page_model_name,  #added article model name  
                'folder_name': get_frontend_folder(internal_page_model_name),  #folder name of the model for frontend url
                'tab_slug': parent_slug, #tab slug of the model for frontend url
                'page_slug': tab_slug, #page slug of the model for frontend url
                'image': image_data,                
                }
            dev_list.append(developer_data)
        return dev_list
 
class FullImageBlockSerializer(serializers.Serializer):
    image = serializers.SerializerMethodField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)    
    
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
    
    
class FullVideoBlockSerializer(serializers.Serializer):
    video_source = serializers.CharField(read_only=True)
    upload_video = serializers.SerializerMethodField(read_only=True)
    external_video_link = serializers.URLField(read_only=True)
    thumbnail = serializers.SerializerMethodField(read_only=True)    
    link_label = serializers.CharField(read_only=True)    
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    component_type = serializers.CharField(read_only=True)    
    
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
    
    
class MultiContentOverlayedBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    main_image = serializers.SerializerMethodField(read_only=True)
    secondary_image = serializers.SerializerMethodField(read_only=True)
    points = BaseContentBlockSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    image_alignment = serializers.CharField(read_only=True)
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


class MultiContentImageBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    points = BaseContentBlockSerializer(many=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    image_alignment = serializers.CharField(read_only=True)
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
    
    def get_image(self, obj):
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

class PropertyListBlockSerializer(serializers.Serializer):
    heading = serializers.CharField(read_only=True)
    sub_heading = serializers.CharField(read_only=True)
    background = serializers.CharField(read_only=True)
    top_padding = serializers.CharField(read_only=True)
    bottom_padding = serializers.CharField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField() 
    
    def get_links(self, instance):
        links = instance.get('links')
        return LinkBlockSerializer(links, many=True).data 
    
    def get_pages(self, instance):
        pages = instance.get('pages')
        property_list = []
        request = self.context['request']
        
        for page in pages:
            # Access the specific instance of the page
            page_specific = page.specific
            reading_time = None
            # Check if the page has an image field
            if hasattr(page_specific, 'banner_image') and page_specific.banner_image:
                image = page_specific.banner_image
                image_data = get_image_rendition(image, 'original')
            else:
                image_data = None  # No image found

            # Check if the page has an first_published_at field
            if hasattr(page_specific, 'date') and page_specific.date:
                date = page_specific.date
                date_data = local_timezone(request,date,"%d-%m-%Y")
            else:
                date_data = local_timezone(request,page_specific.date,"%d-%m-%Y")


            if hasattr(page_specific, 'reading_time') and page_specific.reading_time:
                reading_time = page_specific.reading_time
            internal_page_model_name = page_specific._meta.model_name
            page_parent_page = page_specific.get_parent()
            linked_page = BlogLinkPage.objects.filter(internal_page=page_parent_page).first()
            # print(page.get_parent(),"-------------linked_pages-------------------",linked_page.get_parent())
            tab_slug = ''
            parent_slug = ''
            if linked_page:
                tab_slug = linked_page.slug
                parent_slug = linked_page.get_parent().slug
            property_data = {
                'page_id': page.id, #added article id 
                'page_title': page.title, #added article title 
                'slug': page.slug, #added article slug 
                'date':date_data, #added article first_published_at date 
                'reading_time':reading_time, #added article reading  
                # 'page_type': internal_page_model_name,  #added article model name  
                'folder_name': get_frontend_folder(internal_page_model_name),  #folder name of the model for frontend url
                'tab_slug': parent_slug, #tab slug of the model for frontend url
                'page_slug': tab_slug, #page slug of the model for frontend url
                'image': image_data,                
                }
            property_list.append(property_data)
        return property_list
    
    





# ------------------------------------------------------------   


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
            elif block.block_type == 'normal_image_block':
                content_blocks.append({
                    'type': 'normal_image_block',
                    'value': NormalImageBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'management_msg_block':
                content_blocks.append({
                    'type': 'management_msg_block',
                    'value': ManagementMessageBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'top_management_block':
                content_blocks.append({
                    'type': 'top_management_block',
                    'value': TopManagementListBlockSerializer(block.value, context={'parent': self}).data
                })                
            elif block.block_type == 'management_list_block':
                content_blocks.append({
                    'type': 'management_list_block',
                    'value': ManagementListBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'base_image_block':
                content_blocks.append({
                    'type': 'base_image_block',
                    'value': BaseImageBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'normal_text':
                content_blocks.append({
                    'type': 'normal_text',
                    'value': NormalTextBlockSerializer(block.value, context={'parent': self}).data
                })  
            elif block.block_type == 'feature_list_block':
                content_blocks.append({
                    'type': 'feature_list_block',
                    'value': FeaturesListBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'point_text_block':
                content_blocks.append({
                    'type': 'point_text_block',
                    'value': PointTextBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'why_us_block':
                content_blocks.append({
                    'type': 'why_us_block',
                    'value': WhyUsBlockSerializer(block.value, context={'parent': self}).data
                })  
            elif block.block_type == 'overview_block':
                content_blocks.append({
                    'type': 'overview_block',
                    'value': OverviewBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'contact_info_block':
                content_blocks.append({
                    'type': 'contact_info_block',
                    'value': ContactInfoBlockSerializer(block.value, context={'parent': self}).data
                })   
            elif block.block_type == 'social_share_block':
                content_blocks.append({
                    'type': 'social_share_block',
                    'value': SocialSharingBlockSerializer(block.value, context={'parent': self,'request': request}).data
                })     
            elif block.block_type == 'link_block':
                content_blocks.append({
                    'type': 'link_block',
                    'value': LinkBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'faq_block':
                content_blocks.append({
                    'type': 'faq_block',
                    'value': FAQBlockSerializer(block.value, context={'parent': self}).data
                })                
            elif block.block_type == 'review_card_block':
                content_blocks.append({
                    'type': 'review_card_block',
                    'value': ReviewCardBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'image_card_block':
                content_blocks.append({
                    'type': 'image_card_block',
                    'value': ImageCardSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'text_card_block':
                content_blocks.append({
                    'type': 'text_card_block',
                    'value': TextCardBlockSerializer(block.value, context={'parent': self}).data
                })  
            elif block.block_type == 'profile_card_block':
                content_blocks.append({
                    'type': 'profile_card_block',
                    'value': ProfileCardBlockSerializer(block.value, context={'parent': self}).data
                }) 
            elif block.block_type == 'info_card_block':
                content_blocks.append({
                    'type': 'info_card_block',
                    'value': InfoCardBlockSerializer(block.value, context={'parent': self}).data
                })  
                
            elif block.block_type == 'related_news':
                content_blocks.append({
                    'type': 'related_news',
                    'value': RelatedNewsBlockSerializer(block.value, context={'parent': self}).data
                })
                
            elif block.block_type == 'project_list':
                content_blocks.append({
                    'type': 'project_list',
                    'value': ProjectListBlockSerializer(block.value, context={'parent': self}).data
                })
            elif block.block_type == 'property_list':
                content_blocks.append({
                    'type': 'property_list',
                    'value': PropertyBlockSerializer(block.value, context={'parent': self}).data
                })    
            elif block.block_type == 'agent_list':
                content_blocks.append({
                    'type': 'agent_list',
                    'value': AgentListBlockSerializer(block.value, context={'parent': self}).data
                })
                
            elif block.block_type == 'developer_list':
                content_blocks.append({
                    'type': 'developer_list',
                    'value': DeveloperListBlockSerializer(block.value, context={'parent': self}).data
                })
                
            elif block.block_type == 'overlayed_image_multi_data_list':
                content_blocks.append({
                    'type': 'overlayed_image_multi_data_list',
                    'value': MultiContentOverlayedBlockSerializer(block.value, context={'parent': self}).data
                })
                
            elif block.block_type == 'single_image_multi_data_list':
                content_blocks.append({
                    'type': 'single_image_multi_data_list',
                    'value': MultiContentImageBlockSerializer(block.value, context={'parent': self}).data
                })
            
        return content_blocks