from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Event, Person, Source, Tree
from .forms import EventForm, PersonForm, SourceForm, TreeForm
from pprint import pprint

####################################################################################
## Views
####################################################################################
def index(request):
    trees = Tree.objects.order_by("-created_date") #[:5]
    context = { 'trees': trees }
    return render(request, 'ancestry/index.html', context)

def tree(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)

    def get_parents(member):
        node = {
            "name": member.name,
            "class": "node",
            "textClass": "nodeText",
            "marriages": []
        }

        if not member.father and not member.mother:
            return node

        if member.father:
            father_node = {
                "name": member.father.name,
                "class": "node",
                "textClass": "nodeText",
                "marriages": []
            }
            if member.father.father or member.father.mother:
                paternal_grandparents = get_parents(member.father)
                father_node["marriages"].append({
                    "spouse": {
                        "name": paternal_grandparents.get("name", "NONE"),
                        "class": "node",
                        "textClass": "nodeText"
                    },
                    "children": paternal_grandparents.get("marriages", [])[0].get("children", []) if paternal_grandparents.get("marriages") else []
                })
        else:
            father_node = {"name": "NONE", "class": "node", "textClass": "nodeText"}

        if member.mother:
            mother_node = {
                "name": member.mother.name,
                "class": "node",
                "textClass": "nodeText",
                "marriages": []
            }
            if member.mother.father or member.mother.mother:
                maternal_grandparents = get_parents(member.mother)
                mother_node["marriages"].append({
                    "spouse": {
                        "name": maternal_grandparents.get("name", "NONE"),
                        "class": "node",
                        "textClass": "nodeText"
                    },
                    "children": maternal_grandparents.get("marriages", [])[0].get("children", []) if maternal_grandparents.get("marriages") else []
                })
        else:
            mother_node = {"name": "NONE", "class": "node", "textClass": "nodeText"}

        node["marriages"].append({
            "spouse": mother_node,
            "children": [father_node, mother_node]
        })

        return node

    # Usage
    root_member = tree.members.get(id=1)
    tree_data = get_parents(root_member)
    # print('TREE DATA')
    # pprint(tree_data)

    # Check if tree member has children

    # def get_children(person):
    #     return [{
    #         "name": child.name,
    #         "id": child.id,
    #         "children": get_children(child)
    #     } for child in person.children()]

    # tree_data = [{
    #     "name": member.name,
    #     "id": member.id,
    #     "children": get_children(member)
    # } for member in root_members]

    context = {
        'tree': tree,
        'tree_data': tree_data
    }
    return render(request, 'ancestry/tree.html', context)

def person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    context = {
        'person': person
    }
    return render(request, 'ancestry/person.html', context)

####################################################################################
## Site Management
####################################################################################
def is_admin(user):
    return user.groups.filter(name='Admins').exists()

@login_required
@user_passes_test(is_admin)
def admin(request):
    trees = Tree.objects.all()
    people = Person.objects.all()
    events = Event.objects.all()
    sources = Source.objects.all()
    context = {
        'events': events,
        'people': people,
        'sources': sources,
        'trees': trees
    }
    return render(request, 'ancestry/admin/admin.html', context)

@login_required
@user_passes_test(is_admin)
def admin_tree(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)
    context = {
        'tree': tree
    }
    return render(request, 'ancestry/admin/tree.html', context)

@login_required
@user_passes_test(is_admin)
def admin_edit_tree(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)

    if request.method == 'POST':
        form = TreeForm(request.POST, instance=tree)
        if form.is_valid():
            form.save()
            return redirect('ancestry:admin_tree', tree_id=tree_id)
    else:
        form = TreeForm(instance=tree)

    context = {
        'form': form,
        'tree': tree,
        'form_action': reverse('ancestry:admin_edit_tree', args=[tree_id])
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_create_tree(request):
    # Check if form has been submitted
    if request.method == 'POST':
        form = TreeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ancestry:admin')
    # Otherwise render blank form
    else:
        form = TreeForm()

    context = {
        'form': form,
        'form_action': reverse('ancestry:admin_create_tree')
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_edit_person(request, tree_id, person_id):
    tree = get_object_or_404(Tree, pk=tree_id)
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('ancestry:admin_tree', tree_id=tree_id)
    else:
        form = PersonForm(instance=person)

    context = {
        'form': form,
        'person': person,
        'tree': tree,
        'form_action': reverse('ancestry:admin_edit_person', args=[tree_id, person_id])
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_create_person(request, tree_id):
    tree = get_object_or_404(Tree, pk=tree_id)

    # Check if form has been submitted
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.tree = tree
            person.save()
            form.save_m2m()
            return redirect('ancestry:admin_tree', tree_id=tree_id)
    # Otherwise render blank form
    else:
        form = PersonForm(initial={'tree': tree})

    context = {
        'form': form,
        'form_action': reverse('ancestry:admin_create_person', args=[tree_id])
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_edit_source(request, source_id):
    source = get_object_or_404(Source, pk=source_id)

    if request.method == 'POST':
        form = SourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return redirect('ancestry:admin')
    else:
        form = SourceForm(instance=source)

    context = {
        'form': form,
        'source': source,
        'form_action': reverse('ancestry:admin_edit_source', args=[source_id])
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_create_source(request):
    # Check if form has been submitted
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.save()
            form.save_m2m()
            return redirect('ancestry:admin')
    # Otherwise render blank form
    else:
        form = SourceForm()

    context = {
        'form': form,
        'form_action': reverse('ancestry:admin_create_source')
    }
    return render(request, 'ancestry/forms.html', context)

@login_required
@user_passes_test(is_admin)
def admin_create_event(request, tree_id, person_id):
    person = get_object_or_404(Person, pk=person_id)

    # Check if form has been submitted
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.person = person
            event.save()
            form.save_m2m()
            return redirect('ancestry:admin_tree', tree_id=tree_id)
    # Otherwise render blank form
    else:
        form = EventForm(initial={'person': person})

    context = {
        'form': form,
        'person': person,
        'form_action': reverse('ancestry:admin_create_event', args=[tree_id, person_id])
    }
    return render(request, 'ancestry/forms.html', context)

####################################################################################
## Authentication
####################################################################################

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ancestry:index')
        else:
            return render(request, 'ancestry/auth/login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'ancestry/auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('ancestry:login')

####################################################################################