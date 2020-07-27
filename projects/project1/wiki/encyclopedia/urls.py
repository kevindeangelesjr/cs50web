from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("update", views.update, name="update"),
    path("random", views.random, name="random"),
    path("<str:entry>", views.entry, name="entry")
]
