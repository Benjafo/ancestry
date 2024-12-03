from django.contrib import admin
from .models import Tree, Person, Event, Source

admin.site.register(Tree)
admin.site.register(Person)
admin.site.register(Event)
admin.site.register(Source)