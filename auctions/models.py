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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    starting_bid = models.FloatField()
    image = models.ImageField(upload_to='auctions/resources/upload')
    date_created = models.DateTimeField(default=datetime.now())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    active_status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_list")
    bid_amount = models.FloatField()
    time_updated = models.DateTimeField(auto_now=True) 
    listing_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids", null=True, blank=True)

    @staticmethod
    def highest_bid(listing_bids, listing_item):
        highest_bid = listing_item.starting_bid
        for bid in listing_bids:
            if bid.bid_amount > highest_bid:
                highest_bid = bid.bid_amount
        return highest_bid

    def __str__(self) -> str:
        return f"Bid ({self.user.username} | {self.listing_item.title}) "

class Commentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    text_comment = models.TextField()
    created = models.DateTimeField(default=datetime.now())

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist")