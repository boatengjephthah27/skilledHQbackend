# Generated by Django 4.2.6 on 2023-11-01 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_rename_manager_id_manager_client_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='technologiesused',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
