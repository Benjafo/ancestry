from django.contrib import admin
from .models import Tree, Person, Event, Source

# Register your models here.
admin.site.register(Tree)
admin.site.register(Person)
admin.site.register(Event)
admin.site.register(Source)