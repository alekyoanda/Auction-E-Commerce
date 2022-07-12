from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.name}"

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    starting_bid = models.FloatField()
    image = models.ImageField(upload_to='auctions/resources/upload')
    date_created = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True, blank=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.FloatField()
    time_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def highest_bid(self):
        highest_bid = Bid.objects.first().bid_amount
        for bid in Bid.objects.all():
            if bid.bid_amount > highest_bid:
                highest_bid = bid.bid_amount
        return highest_bid