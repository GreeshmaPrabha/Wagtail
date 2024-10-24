# Generated by Django 5.0.7 on 2024-10-18 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_trends', '0004_alter_markettrendspage_market_trends'),
        ('wagtailimages', '0026_delete_uploadedimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='markettrendspage',
            name='heading',
        ),
        migrations.RemoveField(
            model_name='markettrendspage',
            name='market_trends',
        ),
        migrations.AddField(
            model_name='markettrendspage',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='markettrendspage',
            name='image',
            field=models.ForeignKey(blank=True, help_text='Award image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
