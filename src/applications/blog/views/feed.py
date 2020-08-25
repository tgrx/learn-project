from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from applications.blog.forms import TweetForm
from applications.blog.models import Tweet
from applications.stats.utils import count_stats


@count_stats
class FeedView(FormMixin, ListView):
    form_class = TweetForm
    model = Tweet
    template_name = "blog/feed.html"
