from datetime import datetime

from django import forms
from django.views.generic import FormView

from project.utils import build_age
from project.utils import build_name
from project.utils import build_query_args
from project.utils import load_user_session


class HelloForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    age = forms.IntegerField(required=False)


class IndexView(FormView):
    template_name = "hello/index.html"
    success_url = "/hello/"
    form_class = HelloForm

    def get_initial(self):
        name, age = self.build_name_age()
        return {
            "name": name or "",
            "age": age or None,
        }

    def get_context_data(self, **kwargs):
        parent_context = super().get_context_data(**kwargs)

        name, age = self.build_name_age()

        year = None
        if age is not None:
            year = datetime.now().year - age

        local_context = {
            "name": name,
            "birth_year": year,
        }
        local_context.update(parent_context)

        return local_context

    def form_valid(self, form):
        self.request.session["name"] = form.cleaned_data["name"]
        self.request.session["age"] = form.cleaned_data["age"]
        return super().form_valid(form)

    def build_name_age(self):
        session = load_user_session(self.request) or build_query_args(self.request)
        name = build_name(session)
        age = build_age(session)
        return name, age
