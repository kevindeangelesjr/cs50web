# Generated by Django 3.0.8 on 2020-08-22 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200822_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name=''),
        ),
    ]