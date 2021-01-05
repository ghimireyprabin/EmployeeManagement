# Generated by Django 2.1 on 2020-12-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createMode', '0008_task_resources'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskreview',
            name='resources',
            field=models.FileField(blank=True, null=True, upload_to='resources'),
        ),
        migrations.AddField(
            model_name='taskreview',
            name='submission_feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]