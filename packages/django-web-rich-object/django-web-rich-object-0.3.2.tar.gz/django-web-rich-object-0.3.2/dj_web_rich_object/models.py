from __future__ import unicode_literals

from urllib.parse import urlparse

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist
from django.utils.safestring import mark_safe

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
import web_rich_object


class Tag(TagBase):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    is_hidden = models.BooleanField(default=False, verbose_name=_("hidden"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag, related_name="%(app_label)s_%(class)s_items",
        on_delete=models.CASCADE
    )


class WebRichObjectQuerySet(models.QuerySet):
    def get_wro_attrs(self, url):
        wro = web_rich_object.WebRichObject(url)
        wro_video = wro.video
        if wro_video:
            wro_video = wro_video.replace('autoplay=1', 'autoplay=0')
        wro_attrs = {
            'title': wro.title,
            'site_name': wro.site_name,
            'description': wro.description,
            'tags': wro.tags,

            'type': wro.type,
            'subtype': wro.subtype,

            'image': wro.image,
            'audio': wro.audio,

            'url': wro.url,
            'base_url': wro.base_url,

            'author': wro.author,
            'created_time': wro.created_time,
            'published_time': wro.published_time,
            'modified_time': wro.modified_time,

            'video': wro_video,
            'video_width': wro.video_width,
            'video_height': wro.video_height,
        }
        return wro_attrs

    def create_from_url(self, url=None, **kwargs):
        wro_attrs = self.get_wro_attrs(url)
        wro_attrs.update(kwargs)
        wro_m2m_attrs = {'tags': wro_attrs.pop('tags')}
        instance = self.create(**wro_attrs)
        instance.tags.add(*wro_m2m_attrs['tags'])
        return instance

    def create_or_update_from_url(self, url, **kwargs):
        if self.filter(base_url=url).exists():
            wro = self.filter(base_url=url).first()
            if wro is not None:
                wro_attrs = self.get_wro_attrs(url)
                wro_m2m_attrs = {'tags': wro_attrs.pop('tags')}
                self.model.objects.filter(id=wro.id).update(**wro_attrs)
                wro.tags.add(*wro_m2m_attrs['tags'])
                return wro
        return self.create_from_url(url=url, **kwargs)


class WebRichObject(models.Model):
    title = models.CharField(max_length=300, verbose_name=_("title"))
    type = models.CharField(max_length=30, verbose_name=_("type"))
    subtype = models.CharField(max_length=30, verbose_name=_("subtype"))
    tags = TaggableManager(through=TaggedItem)

    url = models.TextField(max_length=500, verbose_name=_("URL"))
    base_url = models.TextField(max_length=500, verbose_name=_("Base URL"))

    image = models.TextField(null=True, blank=True, verbose_name=_("image"))
    audio = models.TextField(null=True, blank=True, verbose_name=_("audio"))

    video = models.TextField(null=True, blank=True, verbose_name=_("video"))
    video_width = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("video width"))
    video_height = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("video height"))

    site_name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("site name"))
    description = models.TextField(null=True, blank=True, default='', verbose_name=_("description"))
    author = models.CharField(max_length=100, null=True, blank=True, default=None, verbose_name=_("author"))

    created_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_("created time"))
    published_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_("published time"))
    modified_time = models.DateTimeField(blank=True, null=True, default=None, verbose_name=_("modified time"))

    # Plus
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    objects = WebRichObjectQuerySet.as_manager()

    class Meta:
        app_label = 'dj_web_rich_object'
        verbose_name = _("web rich object")
        verbose_name_plural = _("web rich objects")

    def __str__(self):
        return self.title

    def get_link(self, target='_blank', text=None):
        return mark_safe('<a href="%(url)s" target="%(target)s">%(text)s</a>' % {
            'url': self.url,
            'target': target,
            'text': text or self.url
        })
    get_link.short_description = _('Link')

    def get_image(self, target='_blank', max_height=None, max_width="150px"):
        if not self.image:
            return ''
        return mark_safe('<a href="%(url)s" target="%(target)s"><img src="%(image)s" style="max-height: %(max_height)s; max-width: %(max_width)s;"></a>' % {
            'url': self.image,
            'target': target,
            'image': self.image,
            'max_height': max_height or 'null',
            'max_width': max_width or 'null',
        })
    get_image.short_description = _('Image')

    @property
    def wro(self):
        if not hasattr(self, '_wro'):
            self._wro = web_rich_object.WebRichObject(self.url)
        return self._wro

    @property
    def is_iframe(self):
        if not self.video:
            return False
        url = urlparse(self.video)
        if url.path.endswith('.mp4'):
            return False
        return True

    @property
    def template_name(self):
        return 'wro/widget_%s.html' % self.type

    def get_widget(self, **kwargs):
        context = kwargs.copy()
        context['obj'] = self
        try:
            if self.type == 'video' and self.video is None:
                raise TemplateDoesNotExist("No video provided")
            return mark_safe(render_to_response(self.template_name, context).getvalue().decode())
        except TemplateDoesNotExist:
            return mark_safe(render_to_response('wro/widget_website.html', context).getvalue().decode())
