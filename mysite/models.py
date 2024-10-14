from django.db import models
from django.shortcuts import redirect
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.utils.translation import gettext_lazy as _, get_language
from wagtail.fields import RichTextField
from django.urls import path, reverse
from wagtail.models import Locale
from django.core.exceptions import ValidationError


class BasePage(Page):
    # Page already includes seo_title and search_description (which acts as seo_description)
    seo_type = models.CharField(max_length=255, blank=True, help_text=_("SEO Type"))
    # seo_description = models.CharField(max_length=255, blank=True, help_text=_("SEO Description"))
    seo_keywords = models.CharField(max_length=255, blank=True, help_text=_("Comma-separated keywords"))
    canonical_url = models.CharField(max_length=255, blank=True, help_text=_("Canonical URL for this page"))
    og_title = models.CharField(max_length=255, blank=True, help_text=_("Optional. Alternative text for the OG title."))
    og_description = models.CharField(max_length=255, blank=True, help_text=_("Optional. Alternative text for the OG description."))
    og_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('seo_type'),
            # FieldPanel('seo_description'),
            FieldPanel('seo_keywords'),
            FieldPanel('canonical_url'),
            FieldPanel('og_title'),
            FieldPanel('og_description'),
            FieldPanel('og_image'),
        ], heading="SEO Settings"),
    ]

    class Meta:
        abstract = True

    def get_locale(self, request=None):
        if hasattr(self, 'locale') and self.locale:
            return self.locale.language_code
        if request:
            return get_language()
        return 'en'

    # def get_url(self, request=None, current_site=None):
    #     locale = self.get_locale(request)
    #     return reverse('external-redirect', kwargs={'locale':locale,'slug': self.slug})
    
    # def serve_preview(self, request, mode_name):
    #     return redirect(self.get_url(request))
    

    # def get_url_parts(self, request=None):
    #     site_id, root_url, page_path = super().get_url_parts(request)
    #     locale = self.get_locale(request)
    #     new_page_path = reverse('external-redirect', kwargs={'locale': locale, 'slug': self.slug})
    #     return site_id, root_url, new_page_path
    
    def clean(self):
        super().clean()
        slug = self.slug
        # print(Page.objects.filter(slug=slug, locale=self.locale).specific().exclude(id=self.id),"----------ddd------------------------",self.locale)
        # Check if a page with this layout already exists under the parent
    
        if Page.objects.filter(slug=slug, locale=self.locale).exclude(id=self.id).exists():
            raise ValidationError({'layout': _('A page with this slug already exists. Please try another one')}) 
   

class BannerMixin(models.Model):
    banner_heading = models.CharField(max_length=250, help_text=_("Banner heading"), default='', verbose_name=_('Banner heading'))
    banner_subheading = models.CharField(max_length=250, null=True, blank=True, help_text=_("Banner sub heading"), default='', verbose_name=_('Banner sub heading'))
    banner_description  = RichTextField(blank=True, editor='default', help_text=_("Banner description"),verbose_name=_('Banner description'))
    banner_header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Banner image"),
        verbose_name=_('Banner Image')
    )

    # Define content panels for admin interface
    banner_panels = [
        FieldPanel('banner_heading'),
        FieldPanel('banner_subheading'),
        FieldPanel('banner_description'),
        FieldPanel("banner_header_image"),
    ]

    class Meta:
        abstract = True  # This ensures the model is used as a mixin, not a standalone model