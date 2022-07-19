from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing_item"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>/make_unactive", views.make_unactive, name="make_unactive"),
    path("listings/<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("listings/<int:listing_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<str:username>/watchlist", views.watchlist, name="watchlist"),
    path("listings/<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("categories", views.category_list, name="category_list"),
    path("categories/<str:category_name>", views.category, name="category")
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)