# PropertyNewPage.objects.filter(slug = 'stunning-views-rare-unit-beach-front')


from django.shortcuts import render
from .models import PropertyNewPage

def modal_content(request, slug):
    # Fetch the property page instance based on the ID
    instance = PropertyNewPage.objects.get(slug=slug)
    
    # Render the modal content template (create this template as needed)
    return render(request, 'mysite/templates/preview_button.html', {'instance': instance})

