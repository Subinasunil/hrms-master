# Generated by Django 5.0.3 on 2024-04-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_nationality'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(max_length=120, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]