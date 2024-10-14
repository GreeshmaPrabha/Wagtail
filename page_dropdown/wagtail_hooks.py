
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html
from . import views

from .models import *

class NewdynamicPageCreateView(CreateView):
    pass

class NewdynamicPageEditView(EditView):
    pass

class NewdynamicPageViewSet(PageListingViewSet):
    model = PropertyDynPage
    icon = 'globe'
    menu_label = 'New Dynamic Page'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('title', 'status_string')
    search_fields = ('title',)

    create_view_class = NewdynamicPageCreateView
    edit_view_class = NewdynamicPageEditView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-dynamic-new-page'),
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-dynamic-new-page'),
        ]

@hooks.register('register_admin_viewset')
def register_dynamic_page_viewset():
    return NewdynamicPageViewSet('dynamic_new_pages')


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/dynamic1.js')
    )