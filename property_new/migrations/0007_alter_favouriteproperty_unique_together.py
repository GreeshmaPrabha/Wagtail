# Generated by Django 5.0.7 on 2024-09-26 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_new', '0006_remove_propertynewpage_is_favourite_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favouriteproperty',
            unique_together=set(),
        ),
    ]
