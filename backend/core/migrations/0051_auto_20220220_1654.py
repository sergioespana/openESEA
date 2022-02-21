# Generated by Django 3.1.6 on 2022-02-20 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_auto_20220220_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyAudit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
                ('sample_size', models.IntegerField()),
                ('status', models.CharField(choices=[('not started', 'not started'), ('question selection', 'question selection'), ('documentation upload', 'documentation upload'), ('response sample', 'response sample'), ('sample overview', 'sample overview'), ('audit progress', 'audit progress'), ('verified', 'verified'), ('rejected', 'rejected')], default='not started', max_length=100)),
                ('account_audit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_audits', to='core.method')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_audits', to='core.survey')),
            ],
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='survey_audit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sample', to='core.surveyaudit'),
        ),
    ]