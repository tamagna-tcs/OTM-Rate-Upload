# Generated by Django 3.2.18 on 2023-05-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csvfile',
            name='csv_command',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]