# Generated by Django 3.2.18 on 2023-05-30 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0005_customer_view_all_template_batch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='view_all_template_batch',
            new_name='view_all_template_batches',
        ),
    ]
