# Generated by Django 4.2 on 2023-05-06 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imaging_hub', '0002_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='ImageGallery',
        ),
    ]
