from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("signup/", views.signup, name="signup"),
    path("create/", views.create_post, name="create_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.follow_toggle, name="follow_toggle"),
    path("chat/<str:username>/", views.chat_room, name="chat_room"),
]
