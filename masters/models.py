from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class Purpose(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('is_active'),
        FieldPanel('created_by'),
        FieldPanel('updated_by'),
    ]

    def __str__(self):
        return self.title

@register_snippet
class Category(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('is_active'),
        FieldPanel('created_by'),
        FieldPanel('updated_by'),
    ]

    def __str__(self):
        return self.title

@register_snippet
class Subcategory(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('category'),
        FieldPanel('is_active'),
        FieldPanel('created_by'),
        FieldPanel('updated_by'),
    ]

    def __str__(self):
        return self.title

@register_snippet
class Developer(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='developer_icon')
    description = models.TextField()
    founded_in = models.IntegerField()
    no_of_projects = models.IntegerField()
    price_from = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255) 
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('icon'),
        FieldPanel('description'),
        FieldPanel('founded_in'),
        FieldPanel('no_of_projects'),
        FieldPanel('price_from'),
        FieldPanel('is_active'),
        FieldPanel('created_by'),
        FieldPanel('updated_by'),
    ]

    def __str__(self):
        return self.title