from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

class ManagementService:
    TEMPLATE_PREFIX = 'ancestry/management'
    SUCCESS_URL = '/ancestry/management'

    @classmethod
    def generate_view_classes(cls, model, fields=None, create_fields=None, update_fields=None):
        create_fields = create_fields or fields
        update_fields = update_fields or fields

        class Create(cls, CreateView):
            template_name = f'{cls.TEMPLATE_PREFIX}/form.html'
            fields = create_fields

        class Read(cls, DetailView):
            template_name = f'{cls.TEMPLATE_PREFIX}/models/{model.__name__.lower()}.html'

        class Update(cls, UpdateView):
            template_name = f'{cls.TEMPLATE_PREFIX}/form.html'
            fields = update_fields

        class Delete(cls, DeleteView):
            template_name = f'{cls.TEMPLATE_PREFIX}/confirm.html'
            fields = []

        for view_class in (Create, Read, Update, Delete):
            view_class.success_url = cls.SUCCESS_URL
            view_class.model = model

        return Create, Read, Update, Delete

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