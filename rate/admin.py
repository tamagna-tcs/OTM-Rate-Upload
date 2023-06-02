from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_key', 'domain', 'allow_admin_rate_upload', 'view_all_template_batches', 'end_date')
    def get_ordering(self, request):
        return ['customer_name']
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('customer', 'group_name', 'attribute1', 'attribute2', 'attribute3', 'attribute4', 'attribute5')
    list_filter = ['customer']
    def get_ordering(self, request):
        return ['customer', 'group_name'] 

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('customer', 'offering_type_name', 'offering_type_description', 'rate_type_name', 'group_name', 'enabled')
    list_filter = ['customer', 'offering_type_name', 'rate_type_name']
    def get_ordering(self, request):
        return ['customer', 'group_name', 'offering_type_name', 'rate_type_name'] 

class TemplateStaticColumnAdmin(admin.ModelAdmin):
    list_display = ('customer', 'template', 'position', 'template_column_name', 'master_column_name', 'enterable', 'default_value', 'required', 'include_in_template', 'enabled')
    list_filter = ['customer', 'template']
    def get_ordering(self, request):
        return ['customer', 'template', 'position'] 

class TemplateDynamicColumnAdmin(admin.ModelAdmin):
    list_display = ('customer', 'template', 'position', 'parameter_name', 'enabled')
    list_filter = ['customer', 'template', 'parameter_name']
    def get_ordering(self, request):
        return ['customer', 'template', 'position']

class TemplateDynamicColumnValueAdmin(admin.ModelAdmin):
    list_display = ('customer', 'template', 'param', 'sequence', 'parameter_value', 'template_column_names', 'master_column_names', 'enabled')
    list_filter = ['customer', 'template', 'param']
    def get_ordering(self, request):
        return ['customer', 'template', 'param', 'sequence'] 

class CsvFileAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sequence', 'name', 'csv_file_name', 'file_identifier', 'has_date_field', 'date_format', 'csv_command', 'auto_remove_duplicates', 'enabled')
    list_filter = ['customer']
    def get_ordering(self, request):
        return ['customer', 'sequence', 'name'] 

class CsvStructureAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'sequence', 'column_name', 'fixed_value', 'source_column_name', 'expression', 'enabled')
    list_filter = ['csv_file']
    def get_ordering(self, request):
        return ['csv_file', 'sequence'] 

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'customer', 'user_type', 'group_name')
    list_filter = ['customer']
    def get_ordering(self, request):
        return ['customer', 'user', 'user_type'] 

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'instance_name', 'instance_type', 'end_date')
    list_filter = ['customer']
    def get_ordering(self, request):
        return ['customer', 'instance_name'] 

class UserAccessAdmin(admin.ModelAdmin):
    list_display = ('customer', 'user', 'instance', 'end_date')
    list_filter = ['customer']
    def get_ordering(self, request):
        return ['customer', 'user', 'instance']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency_code')
    def get_ordering(self, request):
        return ['currency_code']  

class UOMAdmin(admin.ModelAdmin):
    list_display = ('uom_type', 'uom_code', 'description')
    def get_ordering(self, request):
        return ['uom_type', 'uom_code']

class BatchAdmin(admin.ModelAdmin):
    list_display = ('customer', 'template', 'batch_name')
    def get_ordering(self, request):
        return ['customer', 'template', 'batch_name'] 

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(UserAccess, UserAccessAdmin)

admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateStaticColumn, TemplateStaticColumnAdmin)
admin.site.register(TemplateDynamicColumn, TemplateDynamicColumnAdmin)
admin.site.register(TemplateDynamicColumnValue, TemplateDynamicColumnValueAdmin)

admin.site.register(CsvFile, CsvFileAdmin)
admin.site.register(CsvStructure, CsvStructureAdmin)

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(UOM, UOMAdmin)
admin.site.register(Batch, BatchAdmin)
