# Generated by Django 2.1 on 2020-11-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('createMode', '0006_taskrejectfeedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='reject_feedback_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
