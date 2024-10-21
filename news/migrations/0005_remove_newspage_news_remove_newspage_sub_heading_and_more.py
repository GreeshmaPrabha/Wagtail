# Generated by Django 5.0.7 on 2024-10-18 10:31

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_newspage_content_alter_newspage_news'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspage',
            name='news',
        ),
        migrations.RemoveField(
            model_name='newspage',
            name='sub_heading',
        ),
        migrations.AddField(
            model_name='newspage',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='description',
            field=wagtail.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Career image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='newspage',
            name='reading_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Read Time'),
        ),
        migrations.AlterField(
            model_name='newspage',
            name='content',
            field=wagtail.fields.StreamField([('social_share_block', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock(help_text='Add your heading', required=False)), ('sub_heading', wagtail.blocks.CharBlock(help_text='Add sub heading', required=False)), ('background', wagtail.blocks.ChoiceBlock(blank=True, choices=[('transparent', 'Transparent Background'), ('solid', 'Solid Background'), ('gradient', 'Gradient Background'), ('pattern', 'Pattern Background')], help_text='Block Backgound', max_length=50, null=True)), ('top_padding', wagtail.blocks.ChoiceBlock(blank=True, choices=[('big', 'Big (120px/80px/40px)'), ('small', 'Small (64px)'), ('none', 'NO Padding')], help_text='Top padding', max_length=50, null=True)), ('bottom_padding', wagtail.blocks.ChoiceBlock(blank=True, choices=[('big', 'Big (120px/80px/40px)'), ('small', 'Small (64px)'), ('none', 'NO Padding')], help_text='Bottom padding', max_length=50, null=True)), ('alignment', wagtail.blocks.ChoiceBlock(blank=True, choices=[('center', 'Center'), ('right', 'Right'), ('left', 'Left')], help_text='Block Alignment', max_length=20, null=True)), ('social_media', wagtail.blocks.MultipleChoiceBlock(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('linkedin', 'LinkedIn'), ('youtube', 'YouTube')], help_text='Select the social media platforms you want to display.'))], group='Base Blocks'))], blank=True, null=True),
        ),
    ]
