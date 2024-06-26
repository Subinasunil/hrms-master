# Generated by Django 5.0.3 on 2024-03-28 07:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0015_alter_emp_master_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emp_master',
            options={'verbose_name': 'Employee Master', 'verbose_name_plural': 'Employee Masters'},
        ),
        migrations.RemoveField(
            model_name='emp_master',
            name='custom_fields',
        ),
        migrations.CreateModel(
            name='UserDefinedField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_value', models.TextField()),
                ('emp_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_defined_fields', to='EmpManagement.emp_master')),
            ],
            options={
                'verbose_name': 'User Defined Field',
                'verbose_name_plural': 'User Defined Fields',
            },
        ),
    ]
