from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path('register/', views.add_user, name="add_user"),
    path('register/create/', views.treat_post_add_user,
         name="treat"),
    path('login/', views.login_user, name="login"),
    path('login/treat-data', views.treat_post_login, name="treat-login"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
