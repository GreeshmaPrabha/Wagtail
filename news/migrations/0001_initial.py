# Generated by Django 5.0.7 on 2024-10-11 11:52

import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('wagtailcore', '0093_uploadedfile'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('seo_type', models.CharField(blank=True, help_text='SEO Type', max_length=255)),
                ('seo_keywords', models.CharField(blank=True, help_text='Comma-separated keywords', max_length=255)),
                ('canonical_url', models.CharField(blank=True, help_text='Canonical URL for this page', max_length=255)),
                ('og_title', models.CharField(blank=True, help_text='Optional. Alternative text for the OG title.', max_length=255)),
                ('og_description', models.CharField(blank=True, help_text='Optional. Alternative text for the OG description.', max_length=255)),
                ('banner_heading', models.CharField(default='', help_text='Banner heading', max_length=250, verbose_name='Banner heading')),
                ('banner_subheading', models.CharField(blank=True, default='', help_text='Banner sub heading', max_length=250, null=True, verbose_name='Banner sub heading')),
                ('banner_description', wagtail.fields.RichTextField(blank=True, help_text='Banner description', verbose_name='Banner description')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('body', wagtail.fields.RichTextField(blank=True)),
                ('banner_header_image', models.ForeignKey(blank=True, help_text='Banner image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Banner Image')),
                ('og_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'News Index Page',
                'verbose_name_plural': 'News Index Pages',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='NewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('seo_type', models.CharField(blank=True, help_text='SEO Type', max_length=255)),
                ('seo_keywords', models.CharField(blank=True, help_text='Comma-separated keywords', max_length=255)),
                ('canonical_url', models.CharField(blank=True, help_text='Canonical URL for this page', max_length=255)),
                ('og_title', models.CharField(blank=True, help_text='Optional. Alternative text for the OG title.', max_length=255)),
                ('og_description', models.CharField(blank=True, help_text='Optional. Alternative text for the OG description.', max_length=255)),
                ('banner_heading', models.CharField(default='', help_text='Banner heading', max_length=250, verbose_name='Banner heading')),
                ('banner_subheading', models.CharField(blank=True, default='', help_text='Banner sub heading', max_length=250, null=True, verbose_name='Banner sub heading')),
                ('banner_description', wagtail.fields.RichTextField(blank=True, help_text='Banner description', verbose_name='Banner description')),
                ('view_count', models.PositiveIntegerField(default=0, editable=False)),
                ('heading', models.CharField(blank=True, max_length=250, null=True, verbose_name='Heading')),
                ('sub_heading', models.CharField(blank=True, max_length=250, null=True, verbose_name='Sub Heading')),
                ('news_heading', models.CharField(blank=True, max_length=250, null=True, verbose_name='News Heading')),
                ('more_news_heading', models.CharField(blank=True, max_length=250, null=True, verbose_name='More News Heading')),
                ('news', wagtail.fields.StreamField([('news_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('posted_date', wagtail.blocks.CharBlock(help_text='Posted date', required=True)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False))]))])),
                ('content', wagtail.fields.StreamField([('news_content_block', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=False)), ('description', wagtail.blocks.RichTextBlock(editor='default', help_text='Add additional text', required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('industried', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('points', wagtail.blocks.CharBlock(help_text='Add your points', required=False))]), help_text='Add multiple points to this section', label='Add industries'))], group='Base Blocks')), ('news_related_news_block', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=False)), ('related_news', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('page', wagtail.blocks.PageChooserBlock(required=False))]), help_text='Add related news to this section', label='Add pages'))], group='Base Blocks'))], blank=True, null=True)),
                ('banner_header_image', models.ForeignKey(blank=True, help_text='Banner image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Banner Image')),
                ('og_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'News Page',
                'verbose_name_plural': 'News Pages',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='NewsPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='news.newspage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='news.NewsPageTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
