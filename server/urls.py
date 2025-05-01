from django.urls import path
from .views import SearchView, search_cars
from .api_views import SearchAPIView
 
urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('api/search/', SearchAPIView.as_view(), name='api_search'),
    path('api/search_cars/', search_cars, name='search_cars'),
]