from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Category

def listing(request, id):
    listingData = Listings.objects.get(pk=id )
    return render(request, "auctions/listing.html", {
        "listing":listingData,
    })

def index(request):
    active_listings = Listings.objects.filter(available=True)
    return render(request, "auctions/index.html", {
        "active_Listings": active_listings,
        "available_categories" : Category.objects.all(),
    })

def filteredSearch(request):
    if request.method == "POST":
        
        requested_category = request.POST["category"] 
        get_category = Category.objects.get(Category_label=requested_category)
        active_listings = Listings.objects.filter(available=True, item_category=get_category)
        all_available_categories =  Category.objects.all()
        return render(request, "auctions/index.html", {
            "active_Listings" : active_listings,
            "available_categories": all_available_categories,
        })


def NewListing(request):
    if request.method == "GET":
        return render(request, "auctions/createListing.html", {
            "available_categories" : Category.objects.all(),
        })
    else:
        title_InForm = request.POST["title"]
        description_InForm = request.POST["description"]
        price_InForm = request.POST["price"]
        image_url_InForm = request.POST["image_url"]
        category_InForm = request.POST["category"]
        get_category = Category.objects.get(Category_label=category_InForm)
        user_name = request.user

        set_newListing = Listings(
            title = title_InForm,
            item_description = description_InForm,
            asking_price = price_InForm,
            imageUrl = image_url_InForm,
            seller = user_name,
            item_category = get_category
        )

        set_newListing.save()

        return HttpResponseRedirect(reverse(index))





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
