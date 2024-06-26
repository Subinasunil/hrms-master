# Generated by Django 5.0.3 on 2024-03-28 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0018_remove_emp_master_custom_fields_customfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customfield',
            name='EmpMasters',
        ),
        migrations.AddField(
            model_name='customfield',
            name='emp_master',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='custom_fields_customfield', to='EmpManagement.emp_master'),
        ),
        migrations.AddField(
            model_name='emp_master',
            name='custom_fields',
            field=models.ManyToManyField(related_name='emp_masters_customfield', to='EmpManagement.customfield'),
        ),
    ]
