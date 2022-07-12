# Generated by Django 4.0.5 on 2022-07-10 16:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 10, 16, 16, 19, 955056, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(upload_to='auctions/resources/upload'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]