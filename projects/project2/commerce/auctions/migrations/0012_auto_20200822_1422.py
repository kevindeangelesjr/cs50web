# Generated by Django 3.0.8 on 2020-08-22 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200822_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to='media/', verbose_name=''),
        ),
    ]
