from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailimages import blocks as image_blocks
from django.utils import timezone


class ContentPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', image_blocks.ImageChooserBlock()),
    ])
    date = models.DateTimeField(auto_now=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    
class MiniFeedPage(Page):
    
    description = RichTextField()
    
    content_panels = Page.content_panels + [
        FieldPanel('description')]

    subpage_types = ['MiniUpdate']
    
    def updates(self):
        return MiniUpdate.objects.descendant_of(self).live()

class MiniUpdate(Page):
    
    body = RichTextField()
    up_date = models.DateTimeField("Date of Update", default=timezone.now)
    version = models.DecimalField(max_digits=5, decimal_places=3, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        MultiFieldPanel([
            FieldPanel('up_date'),
            FieldPanel('version')],
            heading = 'About This Update')
        ]

    parent_page_types = ['MiniFeedPage']

    template = 'sitepages/content_page.html'

