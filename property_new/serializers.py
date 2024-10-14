
from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.rich_text import RichText
from wagtail.images.models import Image as WagtailImage
from property_new.models import PropertyNewPage, PropertyNewIndexPage,FavouriteProperty
from mysite.utils import get_image_rendition
from bs4 import BeautifulSoup
from django.conf import settings
from mysite.constantvariables import PAGINATION_PERPAGE
from django.core.paginator import Paginator
from django.db import transaction
from mysite.constantvariables import convert_to_choices,CURRENCY_RATES




class PropertyNewBlockSerializer(serializers.Serializer): 
    image_content = serializers.SerializerMethodField()  
    image_content_360 = serializers.SerializerMethodField()
    
    
    def get_image_content_360(self,obj):
        property_media_360 = obj.get('property_media_with_360', [])
        formatted_media = []
        
        for media_item in property_media_360:
            image = media_item.get('image')
            order = media_item.get('order')
            rendition = get_image_rendition(image, 'original')
            if rendition:
                formatted_media.append({
                    'order': order,
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                    })
        return formatted_media
        
        
    
    def get_image_content(self, obj):
        property_media = obj.get('property_media', [])
        formatted_media = []

        for media_item in property_media:
            media_type = media_item.get('media_type')
            is_base = media_item.get('is_base')
            if media_type == 'image':
                image = media_item.get('image')
                rendition = get_image_rendition(image, 'original')
                if rendition:
                    formatted_media.append({
                        'media_type': media_type,
                        'is_base':is_base,
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
                    'is_base':is_base,
                    'url': video.url if video else None,
                    "full_url": settings.BASE_URL + video.url,
                    "alt": video.title
                })

        return formatted_media
    
class PropertyNewMaidBlockSerializer(serializers.Serializer): 
    maid_content = serializers.SerializerMethodField()
    
    def get_maid_content(self, obj):
        try:
            content_data_list = []
            for item in obj['maid_apartment_content']:
                content_data = item['content_data']
                content_data_list.append(content_data)
            
            return content_data_list
        except:
            return None
    
    

# In your main serializer:
class PropertyNewPageSerializer(serializers.ModelSerializer):
    image_content = serializers.SerializerMethodField()
    # maid_content = serializers.SerializerMethodField()
    property_type = serializers.SerializerMethodField()
    type_choice = serializers.SerializerMethodField()
    amount = serializers.CharField(read_only=True)   
    currency_type = serializers.SerializerMethodField()
    property_title = serializers.CharField(read_only=True)   
    property = serializers.CharField(read_only=True)    
    location = serializers.CharField(read_only=True)
    location_block = serializers.SerializerMethodField()
    bedroom_count = serializers.CharField(read_only=True)
    bathroom_count = serializers.CharField(read_only=True)
    plot = serializers.CharField(read_only=True)
    whatsapp = serializers.CharField(read_only=True)
    call_contact = serializers.CharField(read_only=True)    
    # mortgage_description = serializers.CharField(read_only=True)   
    # sale_desc = serializers.CharField(read_only=True)    
    # bua_plot = serializers.CharField(read_only=True)
    # plot_sqft = serializers.CharField(read_only=True)
    # status = serializers.SerializerMethodField()
    # description_title = serializers.CharField(read_only=True)
    # description = serializers.CharField(read_only=True)
    # maid_apartment_title = serializers.CharField(read_only=True) 
    slug = serializers.CharField(read_only=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = PropertyNewPage
        fields = ['id', 'image_content','property_type', 'type_choice', 'amount', 'currency_type', 
                  'property_title', 'property', 'location','location_block', 'bedroom_count', 'bathroom_count',
                  'plot', 'whatsapp', 'call_contact', 
                #   'mortgage_description', 'sale_desc','bua_plot', 
                #   'plot_sqft', 'status', 'description_title', 'description', 'maid_apartment_title','maid_content',
                  'slug','is_favorite']
        
    def get_property_type(self,obj):
        if obj:
            return obj.get_property_type_display()
        
    def get_type_choice(self,obj):
        if obj:
            return obj.get_type_choice_display()
    
    def get_currency_type(self,obj):
        if obj:
            return obj.get_currency_type_display()
    
    def get_status(self,obj):
        if obj:
            return obj.get_status_display()
        
    def get_image_content(self, obj):
        return [
            {
                'type': block.block_type,
                'value': self.serialize_block(block)
            }
            for block in obj.image_content
        ]
    
    def get_location_block(self, obj):
        return [
            {
                'type': block.block_type,
                'value': self.serialize_block(block)
            }
            for block in obj.location_block
        ]
        
    def get_is_favorite(self,obj):
        try:
            request = self.context.get('request')
            # if request.user.is_authenticated:
            return FavouriteProperty.objects.filter(property=obj.id).exists()
        except:
            return False
        
    # def get_maid_content(self, obj):
    #     return [
    #         {
    #             'type': block.block_type,
    #             'value': self.serialize_block(block)
    #         }
    #         for block in obj.maid_content
    #     ]
        
    
    def serialize_block(self, block):
        BLOCK_SERIALIZER_MAP = {
            'property_new_block': PropertyNewBlockSerializer,
            # 'property_new_maid_content_block': PropertyNewMaidBlockSerializer,
            
        }
        serializer_class = BLOCK_SERIALIZER_MAP.get(block.block_type)
        if serializer_class:
            return serializer_class(block.value, context=self.context).data
       
        return block.block.get_api_representation(block.value, self.context['request'])
    
    
class PropertyNewDetailPageSerializer(PropertyNewPageSerializer):
    mortgage_description = serializers.CharField(read_only=True)
    mortgage_duration_type = serializers.SerializerMethodField()
    mortgage_duration = serializers.CharField(read_only=True)
    sale_desc = serializers.CharField(read_only=True)
    bua_plot = serializers.CharField(read_only=True)
    plot_sqft = serializers.CharField(read_only=True)
    status = serializers.SerializerMethodField()
    description_title = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    maid_apartment_title = serializers.CharField(read_only=True)
    mortgage_amount = serializers.SerializerMethodField()

    class Meta(PropertyNewPageSerializer.Meta):
        fields = PropertyNewPageSerializer.Meta.fields + [
            'mortgage_description',
            'mortgage_duration_type',
            'mortgage_duration',
            'sale_desc',
            'bua_plot',
            'plot_sqft',
            'status',
            'description_title',
            'description',
            'maid_apartment_title',
            'mortgage_amount'
        ]
    
    
    def get_status(self,obj):
        if obj:
            return obj.get_status_display()
        
    def get_mortgage_duration_type(self,obj):
        if obj:
            return obj.get_mortgage_duration_type_display()
        
    def get_mortgage_amount(self,obj):
        try:
            type = obj.get_mortgage_duration_type_display()
            duration = obj.mortgage_duration
            amount = obj.amount
            mortgage_amount = float(amount)/float(duration)
            return mortgage_amount
        except:
            return None
    
class PropertyAddtoFavSerializer(serializers.Serializer):
    
    def validate(self, attrs):
        response = {}
        request = self.context['request']
        property_id = self.context['property_id']
        
        if not property_id:           
            response = {"property_id":"Property id is required"}
        
        if response.keys():
            raise serializers.ValidationError(response)

        else:
            return attrs
    
    def save(self):
        request = self.context['request']
        property_id = self.context['property_id']
            
        # user_id = request.user
        user_id = self.context['user_id']
        property_obj = PropertyNewPage.objects.get(id=property_id)
        # user_id = tkt_obj.sender.id
        # attachment_obj = FlightTicketAttachments.objects.select_related("user","flight_ticket").filter(flight_ticket_id=ticket_id,user_id=user_id,file_type=2)
        
        
        with transaction.atomic():
            fav_property_obj = FavouriteProperty.objects.create(
                                    is_favorite = True,
                                    property=property_obj,
                                    user=user_id
                                )
            return fav_property_obj
                
class ChangeCurrencySerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    from_currency = serializers.CharField(required=False)
    to_currency = serializers.CharField(required=True)
    
    def validate(self, attrs):
        request = self.context['request']
        response = {}
        # amount = self.context['amount']
        # from_currency = self.context['from_currency']
        # to_currency = self.context['to_currency']
        if 'amount' in attrs.keys():
            amount = attrs['amount']   
        if 'from_currency' in attrs.keys():
            from_currency = attrs['from_currency']   
        if 'to_currency' in attrs.keys():
            to_currency = attrs['to_currency']   
        if not amount:           
            response = {"amount":"amount is required"}
        if not from_currency:           
            response = {"from_currency":"Current currency is required"}
        if not to_currency:           
            response = {"to_currency":"Currency to change is required"}
        
        if response.keys():
            raise serializers.ValidationError(response)

        else:
            return attrs
    
    def save(self):
        request = self.context['request']
        
        amount = self.validated_data.get('amount')
        from_currency = self.validated_data.get('from_currency')
        to_currency = self.validated_data.get('to_currency')
        try:
            if from_currency == to_currency:
                return amount  # No conversion needed
            else:
                rate = CURRENCY_RATES[from_currency][to_currency]
                new_amnt =  amount * rate
                response = {'new_amnt':new_amnt,'message':'Amount changed'}
                return response
        except:
            raise serializers.ValidationError('some error occured')
        
        
    