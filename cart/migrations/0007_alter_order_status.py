# Generated by Django 4.2.6 on 2023-11-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_cart_duration_of_hire_alter_cart_project_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Nullified', 'Nullified')], max_length=20, null=True),
        ),
    ]