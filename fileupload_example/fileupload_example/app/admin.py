from django.contrib import admin
from .models import WithFile, MultiFileModel, File


admin.site.register(WithFile)
admin.site.register(MultiFileModel)
admin.site.register(File)
