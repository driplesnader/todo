from django.urls import path
from .views import (
    TaskView, TaskUncompletedView, TaskDetailView, TaskTagView,
    TagView, TagDetailView,
)

urlpatterns = [
    path('tasks/', TaskView.as_view()),
    path('tasks/uncompleted/', TaskUncompletedView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tasks/<int:pk>/tags/', TaskTagView.as_view()),
    path('tags/', TagView.as_view()),
    path('tags/<int:pk>/', TagDetailView.as_view()),
]