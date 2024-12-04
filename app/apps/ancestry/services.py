from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PersonForm
from .models import Event, Person, Source, Tree

class ManagementService:
    class TreeCreate(CreateView):
        model = Tree
        template_name = 'ancestry/management/form.html'
        fields = ['name', 'description']
        success_url = '/ancestry/management'

    class TreeRead(DetailView):
        model = Tree
        template_name = 'ancestry/management/management_tree.html'
        success_url = '/ancestry/management'

    class TreeUpdate(UpdateView):
        model = Tree
        template_name = 'ancestry/management/form.html'
        fields = ['description']
        success_url = '/ancestry/management'

    class TreeDelete(DeleteView):
        model = Tree
        template_name = 'ancestry/management/confirm.html'
        fields = []
        success_url = '/ancestry/management'

    class PersonCreate(CreateView):
        model = Person
        template_name = 'ancestry/management/form.html'
        fields = ['name', 'birth_date', 'death_date', 'mother', 'father']
        success_url = '/ancestry/management'

        def form_valid(self, form):
            tree_id = self.kwargs.get('pk')
            form.instance.tree_id = tree_id
            return super().form_valid(form)

    class PersonRead(DetailView):
        model = Person
        template_name = 'ancestry/management/management_person.html'

    class PersonUpdate(UpdateView):
        model = Person
        template_name = 'ancestry/management/form.html'
        form_class=PersonForm

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.object.id})

    class PersonDelete(DeleteView):
        model = Person
        template_name = 'ancestry/management/confirm.html'
        fields = []

        def get_success_url(self):
            return reverse('ancestry:management_read_tree', kwargs={'pk': self.object.tree.id})

    class SourceCreate(CreateView):
        model = Source
        template_name = 'ancestry/management/form.html'
        fields = ['name', 'type', 'date', 'file_location']

        def form_valid(self, form):
            person = Person.objects.get(pk=self.kwargs.get('pk'))
            response = super().form_valid(form)
            person.sources.add(form.instance)
            return response

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

    class SourceRead(DetailView):
        model = Source
        template_name = 'ancestry/management/management_source.html'

    class SourceUpdate(UpdateView):
        model = Source
        template_name = 'ancestry/management/form.html'
        fields = ['name', 'type', 'date', 'file_location']

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

    class SourceDelete(DeleteView):
        model = Source
        template_name = 'ancestry/management/confirm.html'
        fields = []

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

    class EventCreate(CreateView):
        model = Event
        template_name = 'ancestry/management/form.html'
        fields = ['type', 'date']

        def form_valid(self, form):
            person = Person.objects.get(pk=self.kwargs.get('pk'))
            response = super().form_valid(form)
            person.events.add(form.instance)
            return response

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

    class EventRead(DetailView):
        model = Event
        template_name = 'ancestry/management/management_event.html'

    class EventUpdate(UpdateView):
        model = Event
        template_name = 'ancestry/management/form.html'
        fields = ['type', 'date']

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

    class EventDelete(DeleteView):
        model = Event
        template_name = 'ancestry/management/confirm.html'
        fields = []

        def get_success_url(self):
            return reverse('ancestry:management_read_person', kwargs={'pk': self.kwargs['pk']})

class AuthenticationService:
    def login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ancestry:home')
            else:
                return render(request, 'ancestry/auth/login.html', {'error': 'Invalid credentials.'})
        else:
            return render(request, 'ancestry/auth/login.html')

    def logout(request):
        logout(request)
        return redirect('ancestry:login')