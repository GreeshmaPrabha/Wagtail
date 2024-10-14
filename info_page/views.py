from django.shortcuts import redirect, render
from django.urls import path, reverse
from wagtail.models import Locale
from.models import Page
from django.conf import settings

from django.http import JsonResponse
from wagtail import blocks

# Create your views here.
def external_redirect(request,locale, slug):
        try:

            locale_obj = Locale.objects.get(language_code=locale)
            print(settings.FRONTEND_URL,"-----------444-------locale_obj--------------",locale_obj)
            # product = Page.objects.filter(slug=slug,locale=locale_obj).last()
            
            external_url = f"{settings.FRONTEND_URL}/{locale}/preview/{slug}"
            return redirect(external_url)
        except Page.DoesNotExist:
            raise Page("Page not found")
        
