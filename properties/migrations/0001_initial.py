# Generated by Django 5.0.7 on 2024-09-18 11:16

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0093_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('body', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Property Index Page',
                'verbose_name_plural': 'Property Index Pages',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PropertyPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('property_block', wagtail.blocks.StructBlock([('property_images', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False))]))), ('type_choice', wagtail.blocks.ChoiceBlock(choices=['Rent', 'Buy'], label='Select Type')), ('amount', wagtail.blocks.CharBlock(max_length=250, required=False)), ('currency_type', wagtail.blocks.ChoiceBlock(choices=['AED', 'BHD', 'KWD', 'OMR', 'QAR', 'SAR'], label='Select Currency')), ('title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('property', wagtail.blocks.CharBlock(max_length=250, required=False)), ('location', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bedroom_count', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bathroom_count', wagtail.blocks.CharBlock(max_length=250, required=False)), ('plot', wagtail.blocks.CharBlock(max_length=250, required=False)), ('whatsapp', wagtail.blocks.CharBlock(max_length=250, required=False)), ('call_contact', wagtail.blocks.CharBlock(max_length=250, required=False)), ('mortgage_description', wagtail.blocks.CharBlock(max_length=250, required=False)), ('sale_desc', wagtail.blocks.CharBlock(max_length=250, required=False)), ('bua_plot', wagtail.blocks.CharBlock(max_length=250, required=False)), ('plot_sqft', wagtail.blocks.CharBlock(max_length=250, required=False)), ('status', wagtail.blocks.ChoiceBlock(choices=['Completed', 'Pending', 'Inprogress'], label='Select Status')), ('description_title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('description', wagtail.blocks.CharBlock(max_length=250, required=False)), ('maid_apartment_title', wagtail.blocks.CharBlock(max_length=250, required=False)), ('maid_apartment_content', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('content_data', wagtail.blocks.CharBlock(max_length=250, required=False))])))]))])),
            ],
            options={
                'verbose_name': 'Property Page',
                'verbose_name_plural': 'Property Page',
            },
            bases=('wagtailcore.page',),
        ),
    ]
