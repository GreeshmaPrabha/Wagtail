# Generated by Django 5.0.7 on 2024-10-11 11:24

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportpage',
            name='report_heading',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Report Heading'),
        ),
        migrations.AlterField(
            model_name='reportpage',
            name='reports',
            field=wagtail.fields.StreamField([('report_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('posted_date', wagtail.blocks.CharBlock(help_text='Posted date', required=True)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False))]))]),
        ),
    ]
