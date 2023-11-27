# Generated by Django 4.2.6 on 2023-11-06 18:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0009_contract_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='role',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.RemoveField(
            model_name='contract',
            name='talent_ID',
        ),
        migrations.AddField(
            model_name='contract',
            name='talent_ID',
            field=models.ManyToManyField(blank=True, related_name='talent', to=settings.AUTH_USER_MODEL),
        ),
    ]