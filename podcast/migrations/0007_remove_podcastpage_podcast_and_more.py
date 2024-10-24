# Generated by Django 5.0.7 on 2024-10-18 09:46

import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0006_alter_podcastpage_podcast_and_more'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcastpage',
            name='podcast',
        ),
        migrations.RemoveField(
            model_name='podcastpage',
            name='podcast_intro',
        ),
        migrations.AddField(
            model_name='podcastpage',
            name='description',
            field=wagtail.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='podcastpage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Career image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='podcastpage',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Is Featured'),
        ),
        migrations.AddField(
            model_name='podcastpage',
            name='video',
            field=wagtail.fields.StreamField([('video_list_block', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=True)), ('video_source', wagtail.blocks.ChoiceBlock(choices=[('upload', 'Upload Video'), ('external', 'External Video Link')], help_text='Choose whether to upload a video or provide an external link.', label='Video Source')), ('uploaded_video', wagtail.documents.blocks.DocumentChooserBlock(help_text='Upload a video file (MP4, MOV, AVI, or WebM)', label='Upload Video', required=False)), ('external_video_link', wagtail.blocks.URLBlock(help_text='Paste the URL of an external video (e.g., YouTube, Vimeo)', label='External Video Link', required=False)), ('thumbnail', wagtail.images.blocks.ImageChooserBlock(help_text='Choose a thumbnail image for the video.', label='Thumbnail Image')), ('link_label', wagtail.blocks.CharBlock(help_text='The text for the link button.', label='Link Label', max_length=50, required=False))], group='Base Blocks'))], blank=True, null=True),
        ),
    ]
