from django.db import models
from treebeard.mp_tree import MP_Node
# Create your models here.

class Topic(MP_Node):
    name = models.CharField(max_length=100)
    node_order_by = ['name']

    def __str__(self):
        return 'Topic: %s' % self.name


class Exercise(models.Model):
    pass


class Theory(models.Model):
    pass


class Scientist(models.Model):
    pass
