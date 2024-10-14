from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.ui.tables import Column
from django.templatetags.static import static
from django.utils.html import format_html
from .models import InformationIndexPage

class InformationPageCreateView(CreateView):
    pass

class InformationPageEditView(EditView):
    pass

class InformationPageViewSet(PageListingViewSet):
    model = InformationIndexPage
    icon = 'success'
    menu_label = 'Information Pages'
    menu_order = 205
    add_to_settings_menu = False
    exclude_from_explorer = False
    add_to_admin_menu = True
    list_display = ('title', 'status_string')
    search_fields = ('title',)
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),
    ]

    create_view_class = InformationPageCreateView
    edit_view_class = InformationPageEditView

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        return urlpatterns + [
            path('create/', self.create_view_class, name='create'),
            path('<int:page_id>/edit/', self.edit_view_class, name='edit'),
        ]

@hooks.register('register_admin_viewset')
def register_information_page_viewset():
    return InformationPageViewSet('information_pages')

@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
            static('css/preview_blocks.css')
        )


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        static('js/preview_blocks.js')
    )