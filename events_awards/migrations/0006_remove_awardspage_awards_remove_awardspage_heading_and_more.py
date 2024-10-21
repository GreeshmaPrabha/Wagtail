# Generated by Django 5.0.7 on 2024-10-18 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_awards', '0005_remove_awardspage_accolades_and_more'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='awardspage',
            name='awards',
        ),
        migrations.RemoveField(
            model_name='awardspage',
            name='heading',
        ),
        migrations.AddField(
            model_name='awardspage',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Career heading'),
        ),
        migrations.AddField(
            model_name='awardspage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Award image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
