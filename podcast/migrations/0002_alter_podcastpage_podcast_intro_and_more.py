# Generated by Django 5.0.7 on 2024-10-11 11:09

import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastpage',
            name='podcast_intro',
            field=wagtail.fields.StreamField([('podcast_into_block', wagtail.blocks.StructBlock([('video_source', wagtail.blocks.ChoiceBlock(choices=[('upload', 'Upload Video'), ('external', 'External Video Link')], help_text='Choose whether to upload a video or provide an external link.', label='Video Source')), ('uploaded_video', wagtail.documents.blocks.DocumentChooserBlock(help_text='Upload a video file (MP4, MOV, AVI, or WebM)', label='Upload Video', required=False)), ('external_video_link', wagtail.blocks.URLBlock(help_text='Paste the URL of an external video (e.g., YouTube, Vimeo)', label='External Video Link', required=False)), ('watch_time', wagtail.blocks.IntegerBlock(help_text='Estimated time to watch/read the content.', label='Watch Time (minutes)', required=True)), ('thumbnail', wagtail.images.blocks.ImageChooserBlock(help_text='Choose a thumbnail image for the video.', label='Thumbnail Image')), ('date', wagtail.blocks.CharBlock(help_text='Add date', required=False)), ('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=True)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False)), ('points', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('points', wagtail.blocks.CharBlock(help_text='Add your points', required=True))]), help_text='Add multiple points to this section', label='Add text card'))]))]),
        ),
        migrations.AlterField(
            model_name='podcastpage',
            name='sub_heading',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Sub Heading'),
        ),
    ]
