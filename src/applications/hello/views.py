from datetime import datetime
from typing import NamedTuple
from typing import Optional

from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.hello.forms import HelloForm
from applications.stats.utils import count_stats
from project.utils import build_age
from project.utils import build_name
from project.utils import build_query_args
from project.utils import load_user_session


class HelloT(NamedTuple):
    name: str
    age: Optional[int]


@count_stats
class IndexView(FormView):
    template_name = "hello/index.html"
    success_url = reverse_lazy("hello:index")
    form_class = HelloForm

    def get_initial(self):
        data = self.build_name_age()
        return {
            "name": data.name or "",
            "age": data.age or None,
        }

    def get_context_data(self, **kwargs):
        parent_context = super().get_context_data(**kwargs)

        data = self.build_name_age()

        year = None
        if data.age is not None:
            year = datetime.now().year - data.age

        local_context = {
            "name": data.name,
            "birth_year": year,
        }
        local_context.update(parent_context)

        return local_context

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["age"] = form.cleaned_data["age"]
        return super().form_valid(form)

    def build_name_age(self) -> HelloT:
        session = load_user_session(self.request) or build_query_args(self.request)
        name = build_name(session)
        age = build_age(session)
        return HelloT(name=name, age=age)
