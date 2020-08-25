from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.blog.forms import TweetForm
from applications.blog.models import Tweet
from applications.stats.utils import count_stats


@count_stats
class SayView(CreateView):
    form_class = TweetForm
    model = Tweet
    success_url = reverse_lazy("blog:feed")
