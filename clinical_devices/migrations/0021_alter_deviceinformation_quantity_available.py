# Generated by Django 5.1.4 on 2025-03-14 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_devices', '0020_deviceinformation_quantity_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinformation',
            name='quantity_available',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
