# Generated by Django 3.1.6 on 2022-02-20 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_auto_20220220_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountaudit',
            name='assurance_declaration',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]