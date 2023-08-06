from django.contrib import admin
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from dj_web_rich_object import models
from dj_web_rich_object.admin import forms

from taggit import admin as taggit_admin


class WebRichObjectAdmin(admin.ModelAdmin):
    actions = ()
    list_display = ('title', 'get_image', 'get_link', 'site_name', 'type',
                    'subtype', 'tag_list')
    list_filter = ('type', 'create_at', 'updated_at', 'subtype')
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    readonly_fields = ('get_widget',)
    form = forms.WebRichObjectAdminForm
    default_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('title', 'site_name'),
                'author',
                'description',
                'tags',
            )
        }),
        (_("Type"), {
            'fields': (
                ('type', 'subtype'),
            )
        }),
        (_("URLs"), {
            'fields': (
                ('url', 'base_url'),
                ('image', 'audio', 'video'),
            )
        }),
        (_("Dates"), {
            'fields': (
                ('created_time', 'published_time', 'modified_time'),
            )
        }),
        (_("Widget"), {
            'fields': (
                'get_widget',
            )
        }),
    )
    video_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('title', 'site_name'),
                'author',
                'description',
            )
        }),
        (_("Type"), {
            'fields': (
                ('type', 'subtype'),
            )
        }),
        (_("Video"), {
            'fields': (
                'video',
                ('video_width', 'video_height'),
            )
        }),
        (_("URLs"), {
            'fields': (
                ('url', 'base_url'),
                ('image'),
            )
        }),
        (_("Dates"), {
            'fields': (
                ('created_time', 'published_time', 'modified_time'),
            )
        }),
        (_("Widget"), {
            'fields': (
                'get_widget',
            )
        }),
    )

    add_form = forms.WebRichObjectAdminAddForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('url',)
        }),
    )

    list_url = reverse_lazy("admin:dj_web_rich_object_webrichobject")
    detail_url_name = "admin:dj_web_rich_object_webrichobject_choice_change"

    def get_detail_url(self, id_):
        return reverse(self.detail_url_name, kwargs={'object_id': id_})

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.add_fieldsets
        if obj.type.startswith('video'):
            return self.video_fieldsets
        return self.default_fieldsets

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'GET':
            res = super().add_view(request, form_url, extra_context)
            return res
        try:
            form_class = self.get_form(request)
            form = form_class(data=request.POST)
            if form.is_valid():
                wro = form.save()
                form.save_m2m()
                return redirect(self.get_detail_url(wro.id))
            return super().add_view(request, form_url, extra_context)
        except Exception as err:
            msg = 'Error: %s' % (getattr(err, 'message', str(err.args)))
            self.message_user(request, msg, messages.ERROR)
            return redirect(self.list_url)

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def get_image(self, obj):
        return obj.get_image(max_height='75px')
    get_image.short_description = _('Image')


class TaggedItemInline(taggit_admin.TaggedItemInline):
    model = models.TaggedItem


class TagAdmin(taggit_admin.TagAdmin):
    inlines = [TaggedItemInline]
