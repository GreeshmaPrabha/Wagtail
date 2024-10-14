from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks

from .models import CategoryPage

class CategoryPageCreateView(CreateView):
    pass

class CategoryPageEditView(EditView):
    pass

class CategoryPageViewSet(PageListingViewSet):
    model = CategoryPage
    icon = 'globe'
    menu_label = 'Category New Pages'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('title', 'status_string')
    search_fields = ('title',)

    create_view_class = CategoryPageCreateView
    edit_view_class = CategoryPageEditView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-category-new'),
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-category-new'),
        ]

@hooks.register('register_admin_viewset')
def register_trading_page_viewset():
    return CategoryPageViewSet('category_new_pages')