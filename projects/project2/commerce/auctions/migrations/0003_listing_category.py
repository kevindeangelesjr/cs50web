# Generated by Django 3.0.8 on 2020-08-22 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.Category'),
        ),
    ]
