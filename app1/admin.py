from django.contrib import admin
from .models import CustomUser, Organization, Report, Product
from import_export.admin import ImportExportModelAdmin


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  pass


admin.site.register(Product, ProductAdmin)
admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(Report)
