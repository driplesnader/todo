from json import loads
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Task, Tag


class TaskView(View):
    def get(self, request):
        tasks = Task.objects.all()

        result = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'tags': [tag.name for tag in t.tags.all()],
        } for t in tasks]

        return JsonResponse(result, safe=False)

    def post(self, request):
        data = loads(request.body)
        t = Task.objects.create(
            title=data.get('title'),
            description=data.get('description', ''),
            completed=data.get('completed', False),
        )
        return JsonResponse({'id': t.id, 'title': t.title}, status=201)


class TaskUncompletedView(View):
    def get(self, request):
        tasks = Task.objects.filter(completed=False)

        result = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'tags': [tag.name for tag in t.tags.all()],
        } for t in tasks]

        return JsonResponse(result, safe=False)