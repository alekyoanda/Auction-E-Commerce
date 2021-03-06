# Generated by Django 4.0.5 on 2022-07-10 17:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlisting_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FASHION', 'Fashion'), ('SPORT', 'Sport'), ('GAME', 'Game'), ('BOOK', 'Book'), ('ELECTRONIC', 'Electronic'), ('ART & CRAFT', 'Art & Craft'), ('AUTOMOTIVE', 'Automotive'), ('OTHER', 'Other')], default='FASHION', max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 0, 11, 31, 112246)),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
    ]
