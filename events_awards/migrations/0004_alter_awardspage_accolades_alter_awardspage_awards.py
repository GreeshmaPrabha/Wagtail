# Generated by Django 5.0.7 on 2024-10-16 09:06

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_awards', '0003_alter_awardspage_accolades_alter_awardspage_awards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awardspage',
            name='accolades',
            field=wagtail.fields.StreamField([('accolades_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='awardspage',
            name='awards',
            field=wagtail.fields.StreamField([('awards_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False))]))], blank=True, null=True),
        ),
    ]
