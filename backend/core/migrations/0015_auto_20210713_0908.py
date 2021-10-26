# Generated by Django 3.1.6 on 2021-07-13 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210709_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='uiComponent',
            field=models.CharField(choices=[('field', 'field'), ('line', 'line'), ('textbox', 'textbox'), ('checkbox', 'checkbox'), ('dropdown', 'dropdown'), ('radiobutton', 'radiobutton')], default='Field', max_length=100),
        ),
    ]
