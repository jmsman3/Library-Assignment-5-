# Generated by Django 5.0.6 on 2024-08-12 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0007_alter_bookmodel_price'),
        ('Payment', '0003_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Book.bookmodel'),
        ),
    ]
