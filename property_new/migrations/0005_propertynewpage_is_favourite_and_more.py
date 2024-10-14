# Generated by Django 5.0.7 on 2024-09-24 06:40

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_new', '0004_propertynewpage_data_block_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertynewpage',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='propertynewpage',
            name='image_content',
            field=wagtail.fields.StreamField([('property_new_block', wagtail.blocks.StructBlock([('property_media', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('media_type', wagtail.blocks.ChoiceBlock(choices=[('image', 'Image'), ('video', 'Video')])), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('video', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('is_base', wagtail.blocks.BooleanBlock(default=False, help_text='Check if this is the base media.', required=False))])))]))], blank=True, null=True),
        ),
    ]
