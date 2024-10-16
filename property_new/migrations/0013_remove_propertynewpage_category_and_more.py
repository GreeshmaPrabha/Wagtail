# Generated by Django 5.0.7 on 2024-10-04 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_new', '0012_remove_propertynewpage_category_page_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertynewpage',
            name='category',
        ),
        migrations.RemoveField(
            model_name='propertynewpage',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='propertynewpage',
            name='type_choice',
            field=models.CharField(blank=True, choices=[('1', 'Rent'), ('2', 'Buy')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='propertynewpage',
            name='property_type',
            field=models.CharField(blank=True, choices=[('1', 'Apartment'), ('2', 'Commercial-Floors'), ('3', 'Duplexs'), ('4', 'Hotel-Apartments'), ('5', 'Offices'), ('6', 'Penthouses')], max_length=20, null=True),
        ),
    ]
