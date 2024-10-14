from django.conf import settings
from django.core.cache import cache
from wagtail.images.models import Image

def get_image_rendition(image, rendition_spec, cache_timeout=3600):
    if not image:
        return None

    cache_key = f"image_{image.id}_{rendition_spec}"
    data = cache.get(cache_key)
    if not data:
        try:
            rendition = image.get_rendition(rendition_spec)
            full_url = settings.BASE_URL + rendition.url
            data = {
                "url": rendition.url,
                "full_url": full_url,
                "width": rendition.width,
                "height": rendition.height,
                "alt": image.title
            }
            cache.set(cache_key, data, timeout=cache_timeout)  # Cache for specified timeout
        except Exception as e:
            print(f"Error generating image rendition ({rendition_spec}):", e)
            return None
    return data