# Generated by Django 4.2.7 on 2023-11-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0019_alter_contract_contract_file_delete_contractfiles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='working_hours',
            new_name='working_hours_per_week',
        ),
    ]
