# Generated by Django 4.2.6 on 2023-11-06 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0010_alter_contract_role_remove_contract_talent_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='talent_ID',
        ),
        migrations.AddField(
            model_name='contract',
            name='talent_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='talent', to=settings.AUTH_USER_MODEL),
        ),
    ]
