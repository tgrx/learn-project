from django.urls import path

from applications.blog import views
from applications.blog.apps import BlogConfig

app_name = BlogConfig.label

urlpatterns = [
    path("", views.FeedView.as_view(), name="feed"),
    path("tweet/", views.SayView.as_view(), name="say_something"),
    path("tweet/<int:pk>/", views.TweetView.as_view(), name="tweet"),
    path(
        "tweet/<int:pk>/delete/", views.DeleteTweetView.as_view(), name="delete_tweet"
    ),
]
