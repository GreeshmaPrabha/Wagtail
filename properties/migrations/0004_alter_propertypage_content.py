# Generated by Django 5.0.7 on 2024-09-19 04:52

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_alter_propertypage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertypage',
            name='content',
            field=wagtail.fields.StreamField([('property_block', wagtail.blocks.StructBlock([('property_media', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('media_type', wagtail.blocks.ChoiceBlock(choices=[('image', 'Image'), ('video', 'Video')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video', wagtail.documents.blocks.DocumentChooserBlock(required=False))]))), ('property_type', wagtail.blocks.ChoiceBlock(choices=[('Apartment', 'Apartment'), ('Commercial-Floors', 'Commercial-Floors'), ('Duplexs', 'Duplexs'), ('Hotel-Apartments', 'Hotel-Apartments'), ('Offices', 'Offices'), ('Penthouses', 'Penthouses')], label='Select Property Type')), ('type_choice', wagtail.blocks.ChoiceBlock(choices=[('Rent', 'Rent'), ('Buy', 'Buy')], label='Select Type')), ('amount', wagtail.blocks.CharBlock(max_length=250, required=False)), ('currency_type', wagtail.blocks.ChoiceBlock(choices=[('AED', 'AED'), ('BHD', 'BHD'), ('KWD', 'KWD'), ('OMR', 'OMR'), ('QAR', 'QAR'), ('SAR', 'SAR')], label='Select Currency')), ('title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('property', wagtail.blocks.CharBlock(max_length=250, required=False)), ('location', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bedroom_count', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bathroom_count', wagtail.blocks.CharBlock(max_length=250, required=False)), ('plot', wagtail.blocks.CharBlock(max_length=250, required=False)), ('whatsapp', wagtail.blocks.CharBlock(max_length=250, required=False)), ('call_contact', wagtail.blocks.CharBlock(max_length=250, required=False)), ('mortgage_description', wagtail.blocks.CharBlock(max_length=250, required=False)), ('sale_desc', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bua_plot', wagtail.blocks.CharBlock(max_length=250, required=False)), ('plot_sqft', wagtail.blocks.CharBlock(max_length=250, required=False)), ('status', wagtail.blocks.ChoiceBlock(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Inprogress', 'Inprogress')], label='Select Status')), ('description_title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('description', wagtail.blocks.CharBlock(max_length=250, required=False)), ('maid_apartment_title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('maid_apartment_content', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('content_data', wagtail.blocks.CharBlock(max_length=250, required=False))])))]))]),
        ),
    ]
