from django import forms
from django.contrib.admin import widgets as admin_widgets
from dj_web_rich_object import models


class WebRichObjectAdminForm(forms.ModelForm):
    class Meta:
        model = models.WebRichObject
        exclude = ()
        widgets = {
            'image': admin_widgets.AdminURLFieldWidget(),
            'video': admin_widgets.AdminURLFieldWidget(),
            'audio': admin_widgets.AdminURLFieldWidget(),
            'url': admin_widgets.AdminURLFieldWidget(),
            'base_url': admin_widgets.AdminURLFieldWidget()
        }


class WebRichObjectAdminAddForm(forms.ModelForm):
    class Meta(WebRichObjectAdminForm.Meta):
        fields = ('url',)

    def save(self, *args, **kwargs):
        model = self._meta.model
        self.wro = model.objects.create_or_update_from_url(self.cleaned_data['url'])
        return self.wro

    def save_m2m(self):
        pass
