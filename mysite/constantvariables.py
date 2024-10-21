from django.utils.translation import gettext_lazy as _


PROPERTY_TYPE = {
    'Apartment' : 'Apartment',
    'Commercial-Floors' : 'Commercial-Floors',
    'Duplexs' : 'Duplexs',
    'Hotel-Apartments' : 'Hotel-Apartments',
    'Offices' : 'Offices',
    'Penthouses' : 'Penthouses',    
}

TYPE = {
    'Rent' : 'Rent',
    'Buy' : 'Buy',
}

CURRENCY = {
    'AED':'AED',
    'BHD':'BHD',
    'KWD':'KWD',
    'OMR':'OMR',
    'QAR':'QAR',
    'SAR':'SAR',
}

STATUS = {
    'Completed':'Completed',
    'Pending':'Pending',
    'Inprogress':'Inprogress',
}

CURRENCY_RATES = {
    'AED': {'BHD': 0.27, 'KWD': 0.24, 'OMR': 0.10, 'QAR': 1.00, 'SAR': 1.00},
    'BHD': {'AED': 3.75, 'KWD': 0.88, 'OMR': 0.38, 'QAR': 3.75, 'SAR': 3.75},
    'KWD': {'AED': 4.20, 'BHD': 1.14, 'OMR': 0.44, 'QAR': 4.20, 'SAR': 4.20},
    'OMR': {'AED': 10.00, 'BHD': 2.65, 'KWD': 2.30, 'QAR': 10.00, 'SAR': 10.00},
    'QAR': {'AED': 1.00, 'BHD': 0.27, 'KWD': 0.24, 'OMR': 0.10, 'SAR': 1.00},
    'SAR': {'AED': 1.00, 'BHD': 0.27, 'KWD': 0.24, 'OMR': 0.10, 'QAR': 1.00},
}


def convert_to_choices(data_dict):
    return [(key, value) for key, value in data_dict.items()]


PAGINATION_PERPAGE=10


PROFICIENCY_LEVEL_CHOICES = [
    ('beginner', _('Beginner'),),
    ('intermediate', _('Intermediate'),),
    ('advanced', _('Advanced'),),
]

BLOG_INDEX_TARGETS = ['blogs.BlogIndexPage', 
                        'career.CareerIndexPage', 
                        'events_awards.AwardsIndexPage',                        
                        'market_trends.MarketTrendsIndexPage',                                           
                        'more_media.MediaIndexPage',                        
                        'news.NewsIndexPage',
                        'newsletter.NewsLetterIndexPage',                                              
                        'podcast.PodcastIndexPage',
                        'reports.ReportIndexPage'
                    ]

COMPONENT_TYPE = [
        ('mobile', _('App View'),),
	    ('web', _('Web View'),),        
        ('all', _('All'),),
    ]

CARD_CHOICES = [
	    ('2', _('2 cards per row'),),
        ('3', _('3 cards per row'),),
        ('4', _('4 cards per row'),),
    ]

ALIGNMENT_CHOICES = [
        ('center', _('Center'),),
	    ('right', _('Right'),),        
        ('left', _('Left'),),
    ]

PAGE_TARGETS = [ ]


BG_CHOICES = [
        ('transparent', _('Transparent Background'),),
	    ('solid', _('Solid Background'),),        
        ('gradient', _('Gradient Background'),),
        ('pattern', _('Pattern Background'),),
    ]

TOP_PADDING_CHOICES = [
        ('big', _('Big (120px/80px/40px)'),),
	    ('small', _('Small (64px)'),),        
        ('none', _('NO Padding'),),
    ]

BOTTOM_PADDING_CHOICES = [
        ('big', _('Big (120px/80px/40px)'),),
	    ('small', _('Small (64px)'),),        
        ('none', _('NO Padding'),),  
    ]

SOCIAL_MEDIA_CHOICES = [
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('instagram', 'Instagram'),
    ('linkedin', 'LinkedIn'),
    ('youtube', 'YouTube'),
]