from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.ui.tables import Column
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .views import modal_content
from django.templatetags.static import static





from .models import PropertyNewPage

class PropertyNewPageCreateView(CreateView):
    pass

class PropertyNewPageEditView(EditView):
    pass

class ButtonColumn(Column):
    def get_value(self, instance):
        return mark_safe(
            f'<button class="button" onclick="openModal({instance.id})">Preview</button>'
        )
    
# to add filtering option in wagtail
class PropertyPageFilterSet(PageListingViewSet.filterset_class):
    class Meta:
        model = PropertyNewPage
        fields = {
            'amount': ['range'],
            'property':['icontains'],
            'location':['icontains'],
            # ['range'], ['icontains'], ['exact],  
        }

class PropertyNewPageViewSet(PageListingViewSet):
    model = PropertyNewPage  # Your model
    icon = 'globe'
    menu_label = 'Property New Pages'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    
        
    # Fields that can be searched
    search_fields = ('title')
    # List display fields
    list_display = ('title', 'status_string', 'locale','preview_button')    

    # Define the columns
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),
        Column("amount", label="Amount", sort_key="amount"),
        ButtonColumn("preview_button", label="Preview", sort_key=""),
    ]

    filterset_class = PropertyPageFilterSet

    
    def get_queryset(self):
        return super().get_queryset()

    # Define your custom view classes
    create_view_class = PropertyNewPageCreateView
    edit_view_class = PropertyNewPageEditView
    # preview_view_class = PropertyNewPagePreviewView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class.as_view(), name='create-property-new'),
            path('<int:page_id>/edit/', self.edit_view_class.as_view(), name='edit-property-new'),
            # path('<int:page_id>/preview/', self.preview_view_class.as_view(), name='preview-property-new'),  # Uncomment if needed
        ]
        
    def get_template_names(self):
        return ['mysite/mysite/templates/preview_button.html']


@hooks.register('register_admin_viewset')
def register_property_new_page_viewset():
    return PropertyNewPageViewSet('property_new_pages')


  
    
@hooks.register('insert_global_admin_js',order=200)
def global_admin_js():
    return format_html(
        '<script src="{}"></script>'.format(static('js/preview.js'))
    )
    
@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/dynamic_dropdown.js')
    )