from django.shortcuts import render
from .models import Event, Person, Source, Tree
from .services import AuthenticationService, ManagementService

####################################################################################
## Ancestry
####################################################################################

def home(request):
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

def management(request):
    context = { 'trees': Tree.objects.all() }
    return render(request, 'ancestry/management/management.html', context)

ManagementTreeCreate, ManagementTreeRead, ManagementTreeUpdate, ManagementTreeDelete = ManagementService.TreeCreate, ManagementService.TreeRead, ManagementService.TreeUpdate, ManagementService.TreeDelete

ManagementPersonCreate, ManagementPersonRead, ManagementPersonUpdate, ManagementPersonDelete = ManagementService.PersonCreate, ManagementService.PersonRead, ManagementService.PersonUpdate, ManagementService.PersonDelete

ManagementSourceCreate, ManagementSourceRead, ManagementSourceUpdate, ManagementSourceDelete = ManagementService.SourceCreate, ManagementService.SourceRead, ManagementService.SourceUpdate, ManagementService.SourceDelete

ManagementEventCreate, ManagementEventRead, ManagementEventUpdate, ManagementEventDelete = ManagementService.EventCreate, ManagementService.EventRead, ManagementService.EventUpdate, ManagementService.EventDelete


####################################################################################
## Authentication
####################################################################################

def login(request):
    return AuthenticationService.login(request)

def logout(request):
    return AuthenticationService.logout(request)
