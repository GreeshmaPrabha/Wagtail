# Generated by Django 5.0.7 on 2024-10-11 10:42

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerpage',
            name='careers',
            field=wagtail.fields.StreamField([('career_block', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=True)), ('location', wagtail.blocks.CharBlock(help_text='Add your location', required=True)), ('time', wagtail.blocks.CharBlock(help_text='Posted time', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=True))]))]),
        ),
    ]
