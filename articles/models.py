from django.db import models
from treebeard.mp_tree import MP_Node
from ckeditor.fields import RichTextField
# Create your models here.

class Topic(MP_Node):
    name = models.CharField(max_length=100)
    node_order_by = ['name']

    def __str__(self):
        return 'Topic: %s' % self.name

class Article(models.Model):
    name = models.CharField(max_length=200)
    hard = models.IntegerField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    importancy = models.CharField(max_length=100)
    text = RichTextField()

    def __str__(self):
        return self.name


class Scientist(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
