# Generated by Django 4.2.6 on 2023-11-10 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_alter_social_media_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
