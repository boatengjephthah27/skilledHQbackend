# Generated by Django 4.2.7 on 2023-11-23 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0033_customuser_city_customuser_country_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="city",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="country",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="location_link",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="street",
        ),
        migrations.RemoveField(
            model_name="customuser",
            name="zip",
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("street", models.CharField(blank=True, max_length=100, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "location_link",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("zip", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]