# Generated by Django 5.0.6 on 2024-08-11 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book', '0002_alter_bookmodel_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Book',
            new_name='book',
        ),
        migrations.AlterField(
            model_name='bookmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='templates/media/uploads/'),
        ),
    ]
