from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid", views.bid, name="bid"),
    path("remove_listing", views.remove_listing, name="remove_listing"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("<str:category_name>", views.by_category, name="by_category")
]
