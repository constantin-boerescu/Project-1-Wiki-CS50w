from django.urls import path

from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("search/", views.search_result, name="search_result")

]
