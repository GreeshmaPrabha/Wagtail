from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks

from .models import PropertyPage

class PropertyPageCreateView(CreateView):
    pass

class PropertyPageEditView(EditView):
    pass

class PropertyPageViewSet(PageListingViewSet):
    model = PropertyPage
    icon = 'globe'
    menu_label = 'Property Pages'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('title', 'status_string')
    search_fields = ('title',)

    create_view_class = PropertyPageCreateView
    edit_view_class = PropertyPageEditView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-property'),
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-property'),
        ]

@hooks.register('register_admin_viewset')
def register_trading_page_viewset():
    return PropertyPageViewSet('property_pages')