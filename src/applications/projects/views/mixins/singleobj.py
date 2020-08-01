from django import forms
from django.db.models import Model


class SingleObjectMixin:
    model = None
    pk_attr = "pk"

    def get_object_id(self) -> str:
        oid = self.kwargs[self.pk_attr]
        return oid

    def get_object(self) -> Model:
        oid = self.get_object_id()
        obj = self.model.objects.filter(pk=oid).first()
        return obj

    @classmethod
    def update_object(cls, obj, form: forms.Form) -> None:
        for attr, value in form.cleaned_data.items():
            setattr(obj, attr, value)
