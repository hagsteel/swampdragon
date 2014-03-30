from django.contrib import admin
from .models import Company, Staff, Document, CompanyOwner


admin.site.register(Company)
admin.site.register(CompanyOwner)
admin.site.register(Staff)
admin.site.register(Document)
