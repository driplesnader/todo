from json import loads
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Task, Tag


@method_decorator(csrf_exempt, name='dispatch')
class TaskView(View):

    def get(self, request):
        tasks = Task.objects.all()

        tag = request.GET.get('tag')
        if tag:
            tasks = tasks.filter(tags__name=tag)

        result = [{
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'tags': [tag.name for tag in t.tags.all()],
        } for t in tasks.distinct()]

        return JsonResponse(result, safe=False)

    def post(self, request):
        data = loads(request.body)
        t = Task.objects.create(
            title=data.get('title'),
            description=data.get('description', ''),
            completed=data.get('completed', False),
        )

        tag_ids = data.get('tag_ids', [])
        for tag_id in tag_ids:
            tag = get_object_or_404(Tag, pk=tag_id)
            t.tags.add(tag)

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


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):

    def get(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        return JsonResponse({
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'completed': t.completed,
            'tags': [tag.name for tag in t.tags.all()],
        })

    def put(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        data = loads(request.body)
        t.title = data.get('title', t.title)
        t.description = data.get('description', t.description)
        t.completed = data.get('completed', t.completed)
        t.save()

        if 'tag_ids' in data:
            t.tags.clear()
            for tag_id in data['tag_ids']:
                tag = get_object_or_404(Tag, pk=tag_id)
                t.tags.add(tag)

        return self.get(request, pk)

    def patch(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        data = loads(request.body)

        if 'title' in data:
            t.title = data['title']
        if 'description' in data:
            t.description = data['description']
        if 'completed' in data:
            t.completed = data['completed']
        t.save()

        if 'tag_ids' in data:
            for tag_id in data['tag_ids']:
                tag = get_object_or_404(Tag, pk=tag_id)
                t.tags.add(tag)

        return self.get(request, pk)

    def delete(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        t.delete()
        return JsonResponse({'status': 'deleted'})


@method_decorator(csrf_exempt, name='dispatch')
class TaskTagView(View):

    def get(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        tags = [{'id': tag.id, 'name': tag.name, 'color': tag.color}
                for tag in t.tags.all()]
        return JsonResponse(tags, safe=False)

    def post(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        data = loads(request.body)
        tag_ids = data.get('tag_ids', [])

        if not tag_ids:
            return JsonResponse({'status': 400, 'error': 'tag_ids required'}, status=400)

        for tag_id in tag_ids:
            tag = get_object_or_404(Tag, pk=tag_id)
            t.tags.add(tag)

        return self.get(request, pk)

    def delete(self, request, pk):
        t = get_object_or_404(Task, pk=pk)
        data = loads(request.body)
        tag_ids = data.get('tag_ids', [])

        if not tag_ids:
            return JsonResponse({'status': 400, 'error': 'tag_ids required'}, status=400)

        for tag_id in tag_ids:
            tag = get_object_or_404(Tag, pk=tag_id)
            t.tags.remove(tag)

        return self.get(request, pk)


@method_decorator(csrf_exempt, name='dispatch')
class TagView(View):

    def get(self, request):
        tags = Tag.objects.all()
        result = [{'id': tag.id, 'name': tag.name, 'color': tag.color}
                  for tag in tags]
        return JsonResponse(result, safe=False)

    def post(self, request):
        data = loads(request.body)
        tag = Tag.objects.create(
            name=data.get('name'),
            color=data.get('color', ''),
        )
        return JsonResponse({'id': tag.id, 'name': tag.name}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TagDetailView(View):

    def get(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        return JsonResponse({'id': tag.id, 'name': tag.name, 'color': tag.color})

    def put(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = loads(request.body)
        tag.name = data.get('name', tag.name)
        tag.color = data.get('color', tag.color)
        tag.save()
        return self.get(request, pk)

    def patch(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        data = loads(request.body)
        if 'name' in data:
            tag.name = data['name']
        if 'color' in data:
            tag.color = data['color']
        tag.save()
        return self.get(request, pk)

    def delete(self, request, pk):
        tag = get_object_or_404(Tag, pk=pk)
        tag.delete()
        return JsonResponse({'status': 'deleted'})