# Generated by Django 3.1.2 on 2021-06-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CYO', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adventure',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='itemstyle',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
