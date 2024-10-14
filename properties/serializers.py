
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.rich_text import RichText
from wagtail.images.models import Image as WagtailImage
from properties.models import PropertyPage, PropertyIndexPage
from mysite.utils import get_image_rendition
from bs4 import BeautifulSoup
from django.conf import settings



class PropertyBlockSerializer(serializers.Serializer): 
    property_media = serializers.SerializerMethodField()
    property_type = serializers.CharField(read_only=True)
    type_choice = serializers.CharField(read_only=True)
    amount = serializers.CharField(read_only=True)   
    currency_type = serializers.CharField(read_only=True)   
    title = serializers.CharField(read_only=True)   
    property = serializers.CharField(read_only=True)    
    location = serializers.CharField(read_only=True)
    bedroom_count = serializers.CharField(read_only=True)
    bathroom_count = serializers.CharField(read_only=True)
    plot = serializers.CharField(read_only=True)
    whatsapp = serializers.CharField(read_only=True)
    call_contact = serializers.CharField(read_only=True)    
    
    def get_property_media(self, obj):
        property_media = obj.get('property_media', [])
        formatted_media = []

        for media_item in property_media:
            media_type = media_item.get('media_type')
            if media_type == 'image':
                image = media_item.get('image')
                rendition = get_image_rendition(image, 'original')
                if rendition:
                    formatted_media.append({
                        'media_type': media_type,
                        "url": rendition['url'],
                        "full_url": rendition['full_url'],
                        "width": rendition['width'],
                        "height": rendition['height'],
                        "alt": rendition['alt']
                    })
                    
            elif media_type == 'video':
                video = media_item.get('video')
                formatted_media.append({
                    'media_type': media_type,
                    'url': video.url if video else None,
                    "full_url": settings.BASE_URL + video.url,
                    "alt": video.title
                })

        return formatted_media

# In your main serializer:
class PropertyPageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyPage
        fields = ['id', 'content']
        
    def get_content(self, obj):
        return [
            {
                'type': block.block_type,
                'value': self.serialize_block(block)
            }
            for block in obj.content
        ]
        
    
    def serialize_block(self, block):
        BLOCK_SERIALIZER_MAP = {
            'property_block': PropertyBlockSerializer,
        }
        serializer_class = BLOCK_SERIALIZER_MAP.get(block.block_type)
        if serializer_class:
            return serializer_class(block.value, context=self.context).data
       
        return block.block.get_api_representation(block.value, self.context['request'])
    
    
    
