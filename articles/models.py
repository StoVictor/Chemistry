from django.db import models
from treebeard.mp_tree import MP_Node
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
# Create your models here.

class Topic(MP_Node):
    name = models.CharField(max_length=100)
    node_order_by = ['name']

    def __str__(self):
        return 'Topic: %s' % self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    name = models.CharField(max_length=200)
    EXE_OR_THE_CHOICES = (('exercise','exercise'),('theory','theory'))
    exerciese_or_theory = models.CharField(max_length=50, choices=EXE_OR_THE_CHOICES,blank=True)
    pub_date = models.DateTimeField('date published',
                                    default=datetime.now())
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    HARD_CHOICES = zip( range(1,6), range(1,6) )
    hard = models.IntegerField(choices=HARD_CHOICES, blank=True)
    tags = models.ManyToManyField(Tag)
    text = RichTextUploadingField()
    

    def __str__(self):
        return self.name


class Scientist(models.Model):
    name = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published', default=datetime.now())
    tags = models.ManyToManyField(Tag)
    text = RichTextUploadingField(default='')

    def __str__(self):
        return self.name
    
