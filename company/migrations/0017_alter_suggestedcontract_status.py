# Generated by Django 4.2.6 on 2023-11-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_alter_contract_client_id_alter_contract_talent_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestedcontract',
            name='status',
            field=models.CharField(blank=True, choices=[('Awaiting Response', 'Awaiting Response'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], max_length=50, null=True),
        ),
    ]
