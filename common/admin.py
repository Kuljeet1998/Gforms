from django.contrib import admin
from .models import Attachment, ModelA, ModelB
# Register your models here.
admin.site.register(Attachment)
admin.site.register(ModelA)
admin.site.register(ModelB)
