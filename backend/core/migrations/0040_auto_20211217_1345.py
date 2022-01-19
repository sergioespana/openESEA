# Generated by Django 3.1.6 on 2021-12-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20211213_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='directindicator',
            name='cut_off_lower_limit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='directindicator',
            name='cut_off_upper_limit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='indirectindicator',
            name='cut_off_lower_limit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='indirectindicator',
            name='cut_off_upper_limit',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=15, null=True),
        ),
    ]