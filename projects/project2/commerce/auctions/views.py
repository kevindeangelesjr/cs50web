from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Watchlist, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active=True)
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

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        picture = request.POST["picture"]
        lister_id = request.user
        
        listing = Listing(title=title, description=description, lister_id=lister_id, price=price, category=category, picture=picture)
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if user.is_authenticated:
        watchlist_records = Watchlist.objects.filter(watcher_id=user, watchlist__in=[listing]).count()

        if watchlist_records > 0:
            in_watchlist = True
        else:
            in_watchlist = False
    
    else:
        in_watchlist = False
    
    if listing.lister_id == user:
        creator = True
    else:
        creator = False
    
    no_bids = Bid.objects.filter(listing = listing).count()
    highest_bidder = Bid.objects.latest('bid_date')

    comments = Comment.objects.filter(listing = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "no_bids": no_bids,
        "highest_bidder": highest_bidder,
        "creator": creator,
        "comments": comments
    })


def add_watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        user = request.user
        
        watchlist, created = Watchlist.objects.get_or_create(watcher_id = user)
        watchlist.save()
        
        watchlist.watchlist.add(listing)
        watchlist.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        user = request.user
        
        watchlist, created = Watchlist.objects.get_or_create(watcher_id = user)
        watchlist.save()
        
        watchlist.watchlist.remove(listing)
        watchlist.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def watchlist(request):
    user = request.user
    if Watchlist.objects.filter(watcher_id = user).count() == 0:
        listings = []
    else:
        watchlist = Watchlist.objects.get(watcher_id = user)
        listings = watchlist.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        bid = float(request.POST["bid"])
        user = request.user

        if bid <= listing.price:
            return render(request, "auctions/error.html", {
                "message": "ERROR: Bid must be higher than the current price of the item."
            })
        
        else:
            new_bid = Bid(bidder=user, bid=bid, listing=listing)
            new_bid.save()

            listing.price = bid
            listing.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_listing(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))

        listing.active = False
        listing.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def add_comment(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        user = request.user
        comment = request.POST["comment"]

        new_comment = Comment(poster=user, post=comment, listing=listing)
        new_comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def by_category(request, category_name):
    display_category = Category.objects.get(category_name=category_name)
    listings = Listing.objects.filter(category=display_category, active=True)

    return render(request, "auctions/category.html", {
        "category": category_name,
        "listings": listings
    })