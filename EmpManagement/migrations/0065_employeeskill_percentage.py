# Generated by Django 5.0.3 on 2024-04-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpManagement', '0064_languageskill_marketingskill_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeskill',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True),
        ),
    ]
