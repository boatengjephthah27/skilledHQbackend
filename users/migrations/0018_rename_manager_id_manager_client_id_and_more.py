# Generated by Django 4.2.6 on 2023-11-01 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_manager_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='manager_id',
            new_name='client_id',
        ),
        migrations.RenameField(
            model_name='manager',
            old_name='user_id',
            new_name='talent_id',
        ),
    ]
