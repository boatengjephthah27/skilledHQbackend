# Generated by Django 4.2.6 on 2023-11-03 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('contract', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('client_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_ID', to=settings.AUTH_USER_MODEL)),
                ('talent_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talent_ID', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
