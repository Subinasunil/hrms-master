# Generated by Django 5.0.3 on 2024-03-28 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0013_alter_emp_master_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp_master',
            name='user_defined_fields',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.DeleteModel(
            name='UserDefinedField',
        ),
    ]
