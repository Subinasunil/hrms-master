# Generated by Django 5.0.3 on 2024-04-02 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0027_alter_customfield_data_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emp_CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_value', models.CharField(max_length=255)),
                ('data_type', models.CharField(blank=True, choices=[('char', 'CharField'), ('date', 'DateField'), ('email', 'EmailField'), ('integer', 'IntegerField'), ('boolean', 'BooleanField')], max_length=20, null=True)),
                ('emp_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EmpManagement.emp_master')),
            ],
        ),
        migrations.DeleteModel(
            name='CustomField',
        ),
    ]