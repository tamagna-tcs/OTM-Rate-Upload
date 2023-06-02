from django.db import IntegrityError, models
from django.contrib.auth.models import User
from django.forms import ValidationError
from fernet_fields import EncryptedCharField
from .utility import generate_key

# Will store customers
# Customer key is a 13 char long unique alpha-numeric value, which is to be auto-populated
class Customer(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    customer_name = models.CharField(max_length=60, blank=False, unique=True)
    customer_key = models.CharField(max_length=16, blank=True, editable=False, unique=True)
    end_date = models.DateField(null=True, blank=True)
    domain = models.CharField(max_length=60, blank=False, unique=True)
    allow_admin_rate_upload = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    view_all_template_batches = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name

    def save(self, *args, **kwargs):
        if not self.customer_key:
            self.customer_key = generate_key(16)
        success = False
        failure_count = 0
        while not success:
            try:
                super(Customer, self).save(*args, **kwargs)
            except IntegrityError:
                 failure_count += 1
                 if failure_count > 5: 
                     raise
                 else:
                     self.customer_key = generate_key(16)
            else:
                 success = True

# Will store user profiles
# Will be linked to customer and user model
class Profile(models.Model):
    USER_TYPE_LIST = [("ADMIN", "Admin"), ("USER", "User")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    user_type = models.CharField(max_length=10, blank=False, choices=USER_TYPE_LIST)
    group_name = models.CharField(max_length=50, blank=True, default="DEFAULT")
    region = models.CharField(max_length=50, blank=True, default="")
    sub_group = models.CharField(max_length=50, blank=True, default="")
    tag = models.CharField(max_length=50, blank=True, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

# Will store OTM instances
# Will be linked to customer
# OTM user password will be stored in encrypted format
class Instance(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    INSTANCE_TYPE_LIST = [("DEV", "DEV"), ("SIT", "SIT"), ("UAT", "UAT"), ("PATCH", "PATCH"), ("PROD", "PROD")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    instance_name = models.CharField(max_length=30, blank=False)
    instance_type = models.CharField(max_length=30, blank=False, choices=INSTANCE_TYPE_LIST)
    otm_url = models.URLField(blank=False)
    otm_user = models.CharField(max_length=30, blank=False)
    otm_password = EncryptedCharField(max_length=1000, blank=False)
    passkey_enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    end_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.instance_name

    class Meta:
        unique_together = (('customer', 'instance_name'),)

# Will store user access of OTM instance
# Will be linked to customer, user and instance
class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, blank=False)
    end_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + self.instance.instance_name

    class Meta:
        verbose_name = "User Access"
        verbose_name_plural = "User Accesses"

        unique_together = (('user', 'instance'),) 


class Group(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")] 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    group_name = models.CharField(max_length=30, blank=False, default="DEFAULT")
    attribute1 = models.CharField(max_length=100, blank=True)
    attribute2 = models.CharField(max_length=100, blank=True)
    attribute3 = models.CharField(max_length=100, blank=True)
    attribute4 = models.CharField(max_length=100, blank=True)
    attribute5 = models.CharField(max_length=100, blank=True)
    attribute6 = models.CharField(max_length=100, blank=True)
    attribute7 = models.CharField(max_length=100, blank=True)
    attribute8 = models.CharField(max_length=100, blank=True)
    attribute9 = models.CharField(max_length=100, blank=True)
    attribute10 = models.CharField(max_length=100, blank=True)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    end_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer) + " - " + self.group_name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

        unique_together = (('customer', 'group_name'),)  

# Will store offering modes and rate types
# Will be linked to customer
class Template(models.Model):
    OFFERING_TYPE_LIST = [("AIR", "Air"), ("FCL", "FCL (Full Container Load)"), ("LCL", "LCL (Less than Container Load)"), ("LTL", "LTL (Less than Truckload)"), ("TL", "TL (Truckload)"),]
    RATE_TYPE_LIST = [("Container", "Container"), ("Flat", "Flat"), ("Volume", "Volume"), ("Weight", "Weight"), ("Weight Break", "Weight Break"),("Discount", "Discount"),]
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")] 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    group_name = models.CharField(max_length=30, blank=True, null=True, default="DEFAULT")
    offering_type_name = models.CharField(max_length=30, blank=False, choices=OFFERING_TYPE_LIST)
    offering_type_description = models.CharField(max_length=30, blank=True)
    rate_type_name = models.CharField(max_length=30, blank=False, choices=RATE_TYPE_LIST)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    end_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer) + " - " + self.offering_type_name + " - " + self.rate_type_name

    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"

        unique_together = (('customer', 'offering_type_name', 'rate_type_name', 'group_name'),)

# Will store the static columns of the template
# Will be linked to customer
# Master column name will be used to map to the output CSV, this will appear in the first row of the Excel, which will be hidden
# Template column name will be displayed in the Excel
# If enterable is Y, then user will be able to provide default value to that field while downloading the template
# If required is Y, then the field will be required (for the able case)
# Default value field will allow user to have default value for that field
class TemplateStaticColumn(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=False)
    template_column_name = models.CharField(max_length=30, blank=False)
    master_column_name = models.CharField(max_length=30, blank=False)    
    enterable = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    required = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    default_value = models.CharField(max_length=200, blank=True)    
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    include_in_template = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    position = models.IntegerField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    @property
    def html_element_name(self):
        return self.template_column_name.strip().replace(" ", "_").lower()

    def __str__(self):
        return self.template_column_name

    class Meta:
        unique_together = (('customer', 'template', 'template_column_name'), )        

        verbose_name = "Template Static Column"
        verbose_name_plural = "Template Static Columns"

# Will store dynamic parameters
# Will be linked to customer and rate type
class TemplateDynamicColumn(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=False)
    parameter_name = models.CharField(max_length=30, blank=False)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    position = models.IntegerField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    @property
    def html_element_name(self):
        return self.parameter_name.strip().replace(" ", "_").lower()

    def __str__(self):
        return self.parameter_name

    class Meta:
        unique_together = (('customer', 'template', 'parameter_name'), )        

        verbose_name = "Template Dynamic Column"
        verbose_name_plural = "Template Dynamic Columns"

# Will store the values for each dynamic parameter
# Will be linked to customer, rate type and dynamic parameter
# template column name will store the list of column headers (pipe delmited) that will be added to the template if this parameter value is selected by the user
# master column names will store the list of column headers (pipe delmited) respectively
class TemplateDynamicColumnValue(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=False)
    param = models.ForeignKey(TemplateDynamicColumn, on_delete=models.CASCADE, blank=False)
    sequence = models.IntegerField(blank=False)
    parameter_value = models.CharField(max_length=30, blank=False)
    default_selected = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    template_column_names = models.CharField(max_length=1000, blank=False)
    master_column_names = models.CharField(max_length=1000, blank=False)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def get_template_columns(self):
        text = self.template_column_names.strip().lstrip("|").rstrip("|").strip()
        if text or len(text) > 0:
            return text.split("|")
        else:
            return []

    def get_master_columns(self):
        text = self.master_column_names.strip().lstrip("|").rstrip("|").strip()
        if text or len(text) > 0:
            return text.split("|")
        else:
            return []

    def clean(self):
        if len(self.template_column_names.split("|")) != len(self.master_column_names.split("|")):
            raise ValidationError("Number of fields in template column name and master column names must match.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.template_column_names

    class Meta:
        unique_together = (('customer', 'template', 'param', 'sequence'), )        

        verbose_name = "Template Dynamic Column Value"
        verbose_name_plural = "Template Dynamic Columns Values"

# Will store the list of CSV files for customers
# Will be linked to cutomer 
class CsvFile(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30, blank=False)
    sequence = models.IntegerField(blank=False)
    csv_file_name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    file_identifier = models.CharField(max_length=30, blank=False)
    has_date_field = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="N")
    date_format = models.CharField(max_length=30, blank=True, default="YYYYMMDDHH24MISS")
    csv_command = models.CharField(max_length=10, blank=False)
    auto_remove_duplicates = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    auto_number_initial_sequence = models.IntegerField(blank=True, null=True)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer.customer_name) + "-" + str(self.name)

    class Meta:
        unique_together = (('customer', 'name'), ('customer', 'csv_file_name'), )        

        verbose_name = "CSV File"
        verbose_name_plural = "CSV Files"

# Will store the list of fields of the CSV files
# Will be linked to CSV file
class CsvStructure(models.Model):
    YES_NO_LIST = [("N", "No"), ("Y", "Yes")]
    csv_file = models.ForeignKey(CsvFile, on_delete=models.CASCADE, blank=False)
    sequence = models.IntegerField(blank=False)
    column_name = models.CharField(max_length=30, blank=False)
    fixed_value = models.CharField(max_length=30, blank=True)
    source_column_name = models.CharField(max_length=30, blank=True)    
    expression = models.TextField(max_length=1000, blank=True)
    enabled = models.CharField(max_length=1, blank=False, choices=YES_NO_LIST, default="Y")
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.csv_file) + "-" + str(self.sequence)

    class Meta:
        unique_together = (('csv_file', 'sequence'),('csv_file', 'column_name'),)        

        verbose_name = "CSV File Field"
        verbose_name_plural = "CSV File Fields"

class Currency(models.Model):
    currency_code = models.CharField(max_length=10, blank=False, unique=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

class UOM(models.Model):
    UOM_TYPE_LIST = [("VOLUME", "Volume"), ("WEIGHT", "Weight")]
    uom_type = models.CharField(max_length=20, blank=False, choices=UOM_TYPE_LIST)
    uom_code = models.CharField(max_length=10, blank=False)
    description = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = (('uom_type', 'uom_code'),)        

        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"

class Batch(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, blank=False)
    batch_name = models.CharField(max_length=60, blank=False)
    field_values = models.CharField(max_length=200, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.batch_name

    class Meta:
        unique_together = (('customer', 'template', 'batch_name'), )        

        verbose_name = "Batch"
        verbose_name_plural = "Batches"