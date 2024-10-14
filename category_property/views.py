from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import CategoryPage

@require_GET
def get_categories(request):
    property_type = request.GET.get('property_type')
    categories = []
    for category_page in CategoryPage.objects.all():
        for block in category_page.category_details:
            if block.block_type == 'category_facilities' and block.value['property_type'] == property_type:
                categories.append({
                    'value': block.value['category'],
                    'label': block.value['category']
                })
    return JsonResponse({'categories': categories})

@require_GET
def get_subcategories(request):
    category = request.GET.get('category')
    subcategories = []
    for category_page in CategoryPage.objects.all():
        for block in category_page.category_details:
            if block.block_type == 'category_facilities' and block.value['category'] == category:
                for sub_cat in block.value['sub_category']:
                    subcategories.append({
                        'value': sub_cat['sub_category'],
                        'label': sub_cat['sub_category']
                    })
    return JsonResponse({'subcategories': subcategories})
