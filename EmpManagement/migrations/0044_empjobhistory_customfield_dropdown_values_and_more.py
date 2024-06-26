# Generated by Django 5.0.3 on 2024-04-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0043_empfamily_customfield_dropdown_values_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empjobhistory_customfield',
            name='dropdown_values',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empjobhistory_customfield',
            name='radio_values',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empjobhistory_customfield',
            name='selectbox_values',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='empjobhistory_customfield',
            name='data_type',
            field=models.CharField(blank=True, choices=[('char', 'CharField'), ('date', 'DateField'), ('email', 'EmailField'), ('integer', 'IntegerField'), ('boolean', 'BooleanField'), ('dropdown', 'DropdownField'), ('text', 'TextField'), ('radio', 'RadioButtonField'), ('select', 'SelectBoxField')], max_length=20, null=True),
        ),
    ]
