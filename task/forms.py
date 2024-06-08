from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Task


class TodoForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "important",
        )

    def __init__(self, *args, **kwargs) -> None:
        editable = kwargs.pop('editable', True)
        super().__init__(*args, **kwargs)
        if not editable:
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'disabled'
