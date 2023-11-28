from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path('register/', views.add_user, name="add_user"),
    path('register/create/', views.treat_post_add_user,
         name="treat"),
]