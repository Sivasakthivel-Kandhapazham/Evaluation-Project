# Generated by Django 4.2 on 2023-05-07 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imaging_hub', '0005_alter_imagegallery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagegallery',
            name='created_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagegallery',
            name='created_date',
            field=models.DateTimeField(null=True),
        ),
    ]
