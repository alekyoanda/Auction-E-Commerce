# Generated by Django 4.0.5 on 2022-07-10 17:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category_alter_auctionlisting_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 0, 16, 40, 521844)),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
