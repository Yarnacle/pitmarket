from django.urls import path
from . import views
from .views import ListingList,ListingView,MyListingList

urlpatterns = [
	path('',ListingList.as_view(),name = 'listing-list'),
	path('sell/',views.listing_req,name = 'listing-request'),
	path('my-listings/',MyListingList.as_view(),name = 'my-listing-list'),
	path('my-listings/<int:pk>',ListingView.as_view(),name = 'my-listing-detail'),
	path('listings/<int:pk>',ListingView.as_view(),name = 'listing-detail')
]