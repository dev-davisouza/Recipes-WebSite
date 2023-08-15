from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path('register/', views.add_user, name="add_user")
]
