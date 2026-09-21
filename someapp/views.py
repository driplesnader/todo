from django.http import JsonResponse
from django.views import View
from .models import Task


class TaskView(View):
    def get(self, request):
        tasks = Task.objects.all()

        completed = request.GET.get('completed')
        if completed == 'true':
            tasks = tasks.filter(completed=True)
        elif completed == 'false':
            tasks = tasks.filter(completed=False)

        tag = request.GET.get('tag')
        if tag:
            tasks = tasks.filter(tags__name=tag)

        task_list = []
        for task in tasks:
            task_list.append({
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
            })

        obj = {
            'data': task_list
        }
        return JsonResponse(obj)


