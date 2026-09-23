from django.forms import ModelForm
from .models import Task, Tag


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'tags']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']