from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.category_name}"

class Listing(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    lister_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister_id")
    price = models.DecimalField(max_digits=11, decimal_places=2)
    date_listed = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=7, related_name="category")
    picture = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.lister_id}: {self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.DecimalField(max_digits=11, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder}: {self.bid}"

class Comment(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    post = models.CharField(max_length=1000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster}: {self.post}"

class Watchlist(models.Model):
    watcher_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher_id")
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist")