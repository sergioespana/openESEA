# Generated by Django 3.1.6 on 2022-03-23 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_auto_20220323_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionresponse',
            name='under_audit',
        ),
        migrations.AlterField(
            model_name='questionresponse',
            name='auditstatus',
            field=models.CharField(blank=True, choices=[('Not Under Audit', 'Not Under Audit'), ('Open', 'Open'), ('Awaiting Documentation', 'Awaiting Documentation'), ('Awaiting Correction', 'Awaiting Correction'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Not Under Audit', max_length=100),
        ),
    ]
