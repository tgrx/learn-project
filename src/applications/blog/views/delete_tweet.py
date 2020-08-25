from django.urls import reverse_lazy
from django.views.generic import DeleteView

from applications.blog.models import Tweet
from applications.stats.utils import count_stats


@count_stats
class DeleteTweetView(DeleteView):
    model = Tweet
    success_url = reverse_lazy("blog:feed")
