# Generated by Django 5.0.7 on 2024-10-11 12:07

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_alter_reportpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportpage',
            name='reports',
            field=wagtail.fields.StreamField([('report_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('posted_date', wagtail.blocks.CharBlock(help_text='Posted date', required=True)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False))]))], blank=True, null=True),
        ),
    ]
