from django.shortcuts import render
from .models import Event, Person, Source, Tree
from .services import AuthenticationService, ManagementService

####################################################################################
## Ancestry
####################################################################################

def trees(request):
    trees = Tree.objects.all()[:5]
    context = { 'trees': trees }
    return render(request, 'ancestry/home.html', context)

def tree(request, tree_id):
    tree = Tree.objects.get(pk=tree_id)
    context = { 'tree': tree }
    return render(request, 'ancestry/tree.html', context)

def person(request, person_id):
    person = Person.objects.get(pk=person_id)
    events = []
    sources = []
    context = {
        'person': person,
        'events': events,
        'sources': sources
    }
    return render(request, 'ancestry/person.html', context)

def event(request, person_id, event_id):
    event = Event.objects.get(pk=event_id)
    context = { 'event': event }
    return render(request, 'ancestry/event.html', context)

def source(request, person_id, source_id):
    source = Source.objects.get(pk=source_id)
    context = { 'source': source }
    return render(request, 'ancestry/source.html', context)


####################################################################################
## Management
####################################################################################

def crud_panel(request):
    return render(request, 'ancestry/management/crud_panel.html')

TreeCreate, TreeRead, TreeUpdate, TreeDelete = ManagementService.generate_view_classes(
    model=Tree,
    create_fields=['name', 'description'],
    update_fields=['description']
)

PersonCreate, PersonRead, PersonUpdate, PersonDelete = ManagementService.generate_view_classes(
    model=Person,
    fields=['name', 'birth_date', 'death_date', 'mother', 'father']
)

SourceCreate, SourceRead, SourceUpdate, SourceDelete = ManagementService.generate_view_classes(
    model=Source,
    fields=['name', 'type', 'date', 'file_location']
)

EventCreate, EventRead, EventUpdate, EventDelete = ManagementService.generate_view_classes(
    model=Event,
    fields=['type', 'date'],
)


####################################################################################
## Authentication
####################################################################################

def login(request):
    return AuthenticationService.login(request)

def logout(request):
    return AuthenticationService.logout(request)
