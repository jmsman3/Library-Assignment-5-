# Generated by Django 5.0.6 on 2024-08-10 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlibraryaccount',
            name='reference_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
