# Generated by Django 5.0.7 on 2024-10-07 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0002_developer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='price_from',
            field=models.CharField(max_length=255),
        ),
    ]
