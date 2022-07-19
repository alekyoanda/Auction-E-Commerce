from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Commentary, User, AuctionListing, Bid, Category, Watchlist


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
    current_user = request.user
    is_current_user_highest_bid = False
    listing_item = AuctionListing.objects.get(pk=listing_id)
    is_watchlist = False
    comments = Commentary.objects.filter(listing=listing_item)
    if current_user.is_authenticated:
        is_watchlist = len(Watchlist.objects.filter(user=current_user, listing=listing_item)) != 0

    listing_bids = listing_item.bids.all()
    highest_bid = Bid.highest_bid(listing_bids=listing_bids, listing_item=listing_item)
    message = ""
    if len(listing_bids.filter(bid_amount=highest_bid)) != 0:
        is_current_user_highest_bid = listing_bids.filter(bid_amount=highest_bid).first().user == current_user
        
    if request.method == "POST":
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
        is_current_user_highest_bid = listing_bids.filter(bid_amount=highest_bid).first().user == current_user

        return render(request, "auctions/listing.html", {
            "listing": listing_item,
            "listing_bids": updated_listing_bids,
            "highest_bid": highest_bid,
            "message": message,
            "is_current_user_highest_bid": is_current_user_highest_bid,
            "is_watchlist": is_watchlist,
            "comments": comments
        })
    
    if not current_user.is_authenticated:
        message = "Log in to place a bid"
    return render(request, "auctions/listing.html", {
        "listing": listing_item,
        "listing_bids": listing_bids,
        "highest_bid": highest_bid,
        "is_current_user_highest_bid": is_current_user_highest_bid,
        "is_watchlist": is_watchlist,
        "message": message,
        "comments": comments
    })

def create_listing(request):
    categories = Category.objects.all()

    if (request.method == "POST"):
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.FILES.get("image")
        print(image)
        category_name = request.POST["category"]
        category = Category.objects.get(name=category_name)

        if title == "" or starting_bid == "" or image == None:
            message = "Please fill out all forms that are not optional!"
            return render(request, "auctions/create.html", {
                "message": message,
                "categories": categories
            })
        else:
            new_listing = AuctionListing(user=request.user, title=title, description=description, starting_bid=starting_bid, image=image, category=category)
            new_listing.save()
    
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create.html",{
        "categories": categories
    })

def make_unactive(request, listing_id):
    if request.method == "POST":
        listing_item = AuctionListing.objects.get(pk=listing_id)
        listing_item.active_status = False
        listing_item.save()
        return HttpResponseRedirect(reverse("listing_item", args=[listing_id]))

def add_to_watchlist(request, listing_id):
    if (request.method == "POST"):
        current_user = request.user
        listing_item = AuctionListing.objects.get(pk=listing_id)
        Watchlist.objects.create(user=current_user, listing=listing_item)

        return HttpResponseRedirect(reverse("listing_item", args=[listing_id]))
    
def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        current_user = request.user
        listing_item = AuctionListing.objects.get(pk=listing_id)
        Watchlist.objects.filter(user=current_user, listing=listing_item).delete()

        return HttpResponseRedirect(reverse("listing_item", args=[listing_id]))

def watchlist(request, username):
    current_user = request.user
    watchlist_objects = Watchlist.objects.filter(user=current_user)
    listings = []
    for watchlist in watchlist_objects:
        listings.append(watchlist.listing)

    return render(request, "auctions/index.html", {
        "listings": listings
    })

def add_comment(request, listing_id):
    if request.method == "POST":
        current_user = request.user
        listing_item = AuctionListing.objects.get(pk=listing_id)
        comment_text = request.POST["comment"]

        new_comment = Commentary(user=current_user, listing=listing_item, text_comment=comment_text)
        new_comment.save()

        return HttpResponseRedirect(reverse("listing_item", args=[listing_id]))

def category_list(request):
    categories = Category.objects.all()

    return render(request, "auctions/category_list.html", {
        "categories": categories
    })

def category(request, category_name):
    category = Category.objects.get(name=category_name)
    listings = AuctionListing.objects.filter(category=category)

    return render(request, "auctions/index.html", {
        "listings": listings
    })