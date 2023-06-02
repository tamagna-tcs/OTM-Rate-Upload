from rate.models import *

# Get master customer
master_customer = Customer.objects.get(domain="MASTER")

# Get master templates which should be copied
master_templates = Template.objects.filter(customer=master_customer, offering_type_name = "LTL", rate_type_name="Weight Break")
for master_template in master_templates:
    # Create new template
    template = Template(
        customer=master_customer, 
        offering_type_name="LTL",
        offering_type_description="LTL",
        rate_type_name="Discount",
        group_name="DEFAULT",
        enabled=master_template.enabled
    )
    template.save()
    
    # Get static columns for master customer
    master_static_columns = TemplateStaticColumn.objects.filter(customer=master_customer, template=master_template)
    for master_static_column in master_static_columns:
        # Create new static column
        staticColumn = TemplateStaticColumn(
            customer=master_customer, 
            template=template, 
            template_column_name=master_static_column.template_column_name, 
            master_column_name=master_static_column.master_column_name, 
            enterable=master_static_column.enterable, 
            required=master_static_column.required, 
            default_value=master_static_column.default_value, 
            enabled=master_static_column.enabled, 
            include_in_template=master_static_column.include_in_template, 
            position=master_static_column.position
        )
        staticColumn.save()

    # Get dynamic columns for master customer
    master_dyanmic_columns = TemplateDynamicColumn.objects.filter(customer=master_customer, template=master_template)
    for master_dyanmic_column in master_dyanmic_columns:
        # Create new dynamic column
        dynamicColumn = TemplateDynamicColumn(
            customer=master_customer, 
            template=template, 
            parameter_name=master_dyanmic_column.parameter_name, 
            enabled=master_dyanmic_column.enabled, 
            position=master_dyanmic_column.position
        )
        dynamicColumn.save()

        # Get dynamic column values for master customer
        master_dyanmic_column_values = TemplateDynamicColumnValue.objects.filter(customer=master_customer, template=master_template, param=master_dyanmic_column)
        for master_dyanmic_column_value in master_dyanmic_column_values:
            # Create new dynamic column value
            dynamic_column_value = TemplateDynamicColumnValue(
                customer=master_customer, 
                template=template, 
                param=dynamicColumn, 
                sequence=master_dyanmic_column_value.sequence, 
                parameter_value=master_dyanmic_column_value.parameter_value, 
                default_selected=master_dyanmic_column_value.default_selected, 
                template_column_names=master_dyanmic_column_value.template_column_names, 
                master_column_names=master_dyanmic_column_value.master_column_names, 
                enabled=master_dyanmic_column_value.enabled
            )
            dynamic_column_value.save()

print("Done")