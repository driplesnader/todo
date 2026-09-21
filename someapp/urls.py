from django.urls import path, include
from .views import TaskView

urlpatterns = [
    path('tasks/', TaskView.as_view())
]
