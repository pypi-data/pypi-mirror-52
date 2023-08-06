from django.contrib import admin
from dj_web_rich_object import models
from dj_web_rich_object.admin import modeladmins
from taggit import models as taggit_models


admin.site.register(models.WebRichObject, modeladmins.WebRichObjectAdmin)
admin.site.register(models.Tag, modeladmins.TagAdmin)
admin.site.unregister(taggit_models.Tag)
