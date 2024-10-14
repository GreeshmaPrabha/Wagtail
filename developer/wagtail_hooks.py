from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks

from .models import DeveloperPage

class DeveloperPageCreateView(CreateView):
    pass

class DeveloperPageEditView(EditView):
    pass

class DeveloperPageViewSet(PageListingViewSet):
    model = DeveloperPage
    icon = 'globe'
    menu_label = 'Developer New Pages'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('title', 'status_string')
    search_fields = ('title',)

    create_view_class = DeveloperPageCreateView
    edit_view_class = DeveloperPageEditView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-developer-new'),
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-developer-new'),
        ]

@hooks.register('register_admin_viewset')
def register_trading_page_viewset():
    return DeveloperPageViewSet('developer_new_pages')