from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name= 'tasks', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.title
    
