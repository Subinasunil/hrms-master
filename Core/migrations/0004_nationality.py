# Generated by Django 5.0.3 on 2024-04-19 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_alter_cntry_mstr_country_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N_name', models.CharField(max_length=200, null=True, unique=True)),
            ],
        ),
    ]
