# Generated by Django 4.0.5 on 2022-07-10 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_auctionlisting_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 10, 23, 21, 9, 676651)),
        ),
    ]