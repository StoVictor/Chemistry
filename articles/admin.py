from django import forms

from django.contrib import admin
from .models import Topic, Article, Scientist

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from ckeditor.widgets import CKEditorWidget

# Register your models here.
class MyAdmin(TreeAdmin):
    form = movenodeform_factory(Topic)



admin.site.register(Topic, MyAdmin)
admin.site.register(Article)

admin.site.register(Scientist)
