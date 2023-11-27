# Generated by Django 4.2.6 on 2023-11-01 23:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_skillstack_remove_framework_talent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillstack',
            name='type',
            field=models.CharField(blank=True, choices=[('Language', 'Language'), ('Framework', 'Framework'), ('Platform', 'Platform'), ('Version Control', 'Version Control'), ('Storage', 'Storage'), ('API', 'API'), ('Financial Analysis', 'Financial Analysis'), ('Financial Reporting', 'Financial Reporting'), ('Taxation', 'Taxation'), ('Audit and Assurance', 'Audit and Assurance'), ('Bookkeeping', 'Bookkeeping'), ('Accounting Software', 'Accounting Software'), ('Compliance and Regulation', 'Compliance and Regulation'), ('Analytical Skills', 'Analytical Skills'), ('Personal Care', 'Personal Care'), ('Companionship', 'Companionship'), ('Household Management', 'Household Management'), ('Health Monitoring', 'Health Monitoring'), ('Specialized Care', 'Specialized Care'), ('Cultural Sensitivity', 'Cultural Sensitivity')], max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language', models.CharField(blank=True, max_length=30, null=True)),
                ('talent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='users.talent')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
