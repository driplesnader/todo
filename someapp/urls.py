from django.urls import path
from .views import TaskView, TaskUncompletedView

urlpatterns = [
    path('tasks/', TaskView.as_view()),
    path('tasks/uncompleted/', TaskUncompletedView.as_view()),
]