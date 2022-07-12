from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Bid


def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, listing_id):
    listing_item = AuctionListing.objects.get(pk=listing_id)
    listing_bids = listing_item.bids.all()
    highest_bid = Bid.highest_bid(listing_bids=listing_bids, listing_item=listing_item)
    if request.method == "POST":
        message = ""
        current_user = request.user
        bid_amount = request.POST["bid_amount"]
        if bid_amount == "":
            message = "Please fill the field before place a bid!"
        elif float(bid_amount) < highest_bid:
            message = f"Bid must be greater than {listing_item.starting_bid}!"
        else:
            message = "Success place a bid!"
            current_listing_bid = listing_bids.filter(user=current_user).first()
            if current_listing_bid == None:
                Bid.objects.create(user=current_user, bid_amount=bid_amount, listing_item=listing_item)
            else:
                current_listing_bid.bid_amount = request.POST["bid_amount"]
                current_listing_bid.save()

        updated_listing_bids = listing_item.bids.all()
        highest_bid = Bid.highest_bid(listing_bids=updated_listing_bids, listing_item=listing_item)

        return render(request, "auctions/listing.html", {
            "listing": listing_item,
            "listing_bids": updated_listing_bids,
            "highest_bid": highest_bid,
            "message": message
        })
    
    return render(request, "auctions/listing.html", {
        "listing": listing_item,
        "listing_bids": listing_bids,
        "highest_bid": highest_bid
    })