from django.urls import path
from . import views

urlpatterns = [
    path("", views.main),
    path("main", views.main),
    path("register_user", views.register_user),
    path("login_user", views.login_user),
    path("travels", views.show_trips),
    path("travels/join/<int:id>", views.join_trip),
    path("travels/destination/<int:id>", views.show_destination),
    path("travels/add", views.add_trip),
    path("logout", views.logout)
]