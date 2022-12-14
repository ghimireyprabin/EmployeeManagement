# Generated by Django 2.1 on 2020-11-11 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201102_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeejobinfo',
            name='isManager',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='departmentmanager',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
