# Generated by Django 5.0.7 on 2024-10-18 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0008_alter_careerpage_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='careerpage',
            name='content',
        ),
    ]
