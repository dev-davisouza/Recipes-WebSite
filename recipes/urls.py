from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    # Always the search URL will comes before any URLS.
    path('recipes/search/', views.search, name="search"),
    path('', views.home, name="home"),
    path('recipes/category/<str:category_name>/',
         views.category, name="category"),
    path('recipes/<slug>/', views.recipe, name="recipe"),


]
