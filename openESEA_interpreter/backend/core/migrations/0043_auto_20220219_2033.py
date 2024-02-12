# Generated by Django 3.1.6 on 2022-02-19 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_eseaaccount_verified_surveys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networkmember',
            name='role',
            field=models.IntegerField(choices=[(2, 'network admin'), (1, 'guest'), (3, 'auditor')], default=1),
        ),
    ]