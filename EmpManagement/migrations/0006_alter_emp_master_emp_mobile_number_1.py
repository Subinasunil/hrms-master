# Generated by Django 5.0.3 on 2024-03-22 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0005_alter_emp_master_emp_mobile_number_1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_master',
            name='emp_mobile_number_1',
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]
