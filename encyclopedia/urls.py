from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
    path("edit", views.edit, name="edit"),
    path("update", views.update, name="update"),
    path("random_page", views.random_page, name="random_page"),
    path("<str:title>", views.entry, name="entry")
]
