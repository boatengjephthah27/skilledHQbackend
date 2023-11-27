# Generated by Django 4.2.6 on 2023-11-05 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_duration_of_hire_cart_talent_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='duration_of_hire',
            field=models.CharField(blank=True, choices=[('Less than 1 week', 'Less than 1 week'), ('1 to 4 weeks', '1 to 4 weeks'), ('1 to 3 months', '1 to 3 months'), ('Longer than 6 months', 'Longer than 6 months'), ("I'll decide later", "I'll decide later")], default='Less than 1 week', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='project_type',
            field=models.CharField(blank=True, choices=[('New Project', 'New Project'), ('Existing Project', 'Existing Project'), ("None of the above, I'm just looking to learn more about < SkilledHQ / >", "None of the above, I'm just looking to learn more about < SkilledHQ / >")], default='New Project', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='remote',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='service_role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='talent_start_time',
            field=models.CharField(blank=True, choices=[('Immediately', 'Immediately'), ('In 1 to 2 weeks', 'In 1 to 2 weeks'), ('More than 2 weeks from now', 'More than 2 weeks from now'), ("I'll decide later", "I'll decide later")], default='Immediately', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='working_options',
            field=models.CharField(blank=True, choices=[('Full Time (FT)', 'Full Time (FT)'), ('Part Time (PT)', 'Part Time (PT)'), ("I'll decide later", "I'll decide later")], default='Full Time (FT)', max_length=60, null=True),
        ),
    ]