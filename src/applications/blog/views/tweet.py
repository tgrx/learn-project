from django.views.generic import DetailView

from applications.blog.models import Tweet
from applications.stats.utils import count_stats


@count_stats
class TweetView(DetailView):
    model = Tweet
    template_name = "blog/tweet.html"
