# Import necessary modules from Wagtail and Django
from wagtail.admin.viewsets.pages import PageListingViewSet
from wagtail.admin.views.pages.create import CreateView
from wagtail.admin.views.pages.edit import EditView
from django.urls import path
from wagtail import hooks
from wagtail.admin.viewsets.base import ViewSetGroup
from django.utils.translation import gettext_lazy as _
from wagtail.admin.ui.tables import Column
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from wagtail.snippets.models import register_snippet

# Importing models used in different ViewSets
from .models import CareerPage
from events_awards.models import AwardsPage
from market_trends.models import MarketTrendsPage
from podcast.models import PodcastPage
from reports.models import ReportPage
from news.models import NewsPage 
from newsletter.models import NewsLetterPage 
from blogs.models import BlogPage
from more_media.models import *



class CareerPageCreateView(CreateView):
    pass

class CareerPageEditView(EditView):
    pass

# ViewSet for managing Career Pages in the Wagtail admin interface
class CareerPageViewSet(PageListingViewSet):
    model = CareerPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Career Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'career_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = CareerPageCreateView  # Custom create view
    edit_view_class = CareerPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-career'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-career'),  # URL for editing a blog page
        ]
        
        
class AwardPageCreateView(CreateView):
    pass

class AwardPageEditView(EditView):
    pass

# ViewSet for managing Award Pages in the Wagtail admin interface
class AwardPageViewSet(PageListingViewSet):
    model = AwardsPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Award Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'awards_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = AwardPageCreateView  # Custom create view
    edit_view_class = AwardPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-award'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-award'),  # URL for editing a blog page
        ]
        
  
class MarketTrendsPageCreateView(CreateView):
    pass

class MarketTrendsPageEditView(EditView):
    pass

# ViewSet for managing market trends Pages in the Wagtail admin interface
class MarketTrendsPageViewSet(PageListingViewSet):
    model = MarketTrendsPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Market Trends Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'market_trends_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = MarketTrendsPageCreateView  # Custom create view
    edit_view_class = MarketTrendsPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-event-awrds'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-event-awrds'),  # URL for editing a blog page
        ]
        
 
class PodcastPageCreateView(CreateView):
    pass

class PodcastPageEditView(EditView):
    pass

# ViewSet for managing podcast Pages in the Wagtail admin interface
class PodcastPageViewSet(PageListingViewSet):
    model = PodcastPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Podcast Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'podcast_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = PodcastPageCreateView  # Custom create view
    edit_view_class = PodcastPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-podcast'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-podcast'),  # URL for editing a blog page
        ]
        

class ReportPageCreateView(CreateView):
    pass

class ReportPageEditView(EditView):
    pass

# ViewSet for managing report Pages in the Wagtail admin interface
class ReportPageViewSet(PageListingViewSet):
    model = ReportPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Report Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'report_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = ReportPageCreateView  # Custom create view
    edit_view_class = ReportPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-report'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-report'),  # URL for editing a blog page
        ]
             
             
class NewsPageCreateView(CreateView):
    pass

class NewsPageEditView(EditView):
    pass

# ViewSet for managing news Pages in the Wagtail admin interface
class NewsPageViewSet(PageListingViewSet):
    model = NewsPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'News Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'news_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = NewsPageCreateView  # Custom create view
    edit_view_class = NewsPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-news'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-news'),  # URL for editing a blog page
        ]
        
        
class NewsLetterPageCreateView(CreateView):
    pass

class NewsLetterPageEditView(EditView):
    pass

# ViewSet for managing news Pages in the Wagtail admin interface
class NewsLetterPageViewSet(PageListingViewSet):
    model = NewsLetterPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'NewsLetter Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'newsletter_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = NewsLetterPageCreateView  # Custom create view
    edit_view_class = NewsLetterPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-newsletter'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-newsletter'),  # URL for editing a blog page
        ]

class BlogPageCreateView(CreateView):
    pass

class BlogPageEditView(EditView):
    pass

# ViewSet for managing news Pages in the Wagtail admin interface
class BlogPageViewSet(PageListingViewSet):
    model = BlogPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Blog Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'blog_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = BlogPageCreateView  # Custom create view
    edit_view_class = BlogPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-blog'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-blog'),  # URL for editing a blog page
        ]
            
            
class MediaPageCreateView(CreateView):
    pass

class MediaPageEditView(EditView):
    pass

# ViewSet for managing news Pages in the Wagtail admin interface
class MediaPageViewSet(PageListingViewSet):
    model = MediaPage  # Model associated with this ViewSet
    icon = 'globe'  # Icon for the menu
    menu_label = 'Media Pages'  # Label in the admin menu
    menu_order = 10  # Order in the admin menu
    add_to_settings_menu = False  # Do not add to settings menu
    exclude_from_explorer = False  # Include in the explorer
    list_display = ('title', 'status_string')  # Fields to display in the list
    search_fields = ('title',)  # Fields for the search functionality
    name = 'media_pages'  # Unique name for the ViewSet
    columns = PageListingViewSet.columns + [
        Column("locale", label="Locale", sort_key="locale"),  # Custom column for locale
    ]

    create_view_class = MediaPageCreateView  # Custom create view
    edit_view_class = MediaPageEditView  # Custom edit view

    # Method to define additional URL patterns for creating and editing pages
    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()  # Get the default patterns
        return urlpatterns + [
            path('create/', self.create_view_class, name='create-media'),  # URL for creating a blog page
            path('<int:page_id>/edit/', self.edit_view_class, name='edit-media'),  # URL for editing a blog page
        ]
        
                 
class BlogViewSetGroup(ViewSetGroup):
    menu_label = 'Blogs' # Label in the admin menu
    menu_icon = 'folder-open-inverse' # Icon for the menu
    menu_order = 210 # Order in the admin menu
    items = [
        CareerPageViewSet,
        AwardPageViewSet,
        MarketTrendsPageViewSet,
        PodcastPageViewSet,
        ReportPageViewSet,
        NewsPageViewSet,
        NewsLetterPageViewSet,
        BlogPageViewSet,
        MediaPageViewSet
        
    ]
    
# Register the ViewSetGroup
@hooks.register("register_admin_viewset")
def register_viewset():
    return BlogViewSetGroup()