from django import forms
from .models import Tree, Person, Event, Source

class TreeForm(forms.ModelForm):
    class Meta:
        model = Tree
        fields = ['name']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date', 'death_date', 'mother', 'father', 'sources']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        tree = kwargs.pop('tree', None)
        super(PersonForm, self).__init__(*args, **kwargs)

        if tree:
            self.fields['mother'].queryset = Person.objects.filter(tree=tree)
            self.fields['father'].queryset = Person.objects.filter(tree=tree)

        if self.instance.pk:
            self.fields['mother'].queryset = self.fields['mother'].queryset.exclude(pk=self.instance.pk)
            self.fields['father'].queryset = self.fields['father'].queryset.exclude(pk=self.instance.pk)

            self.fields['events'].queryset = Event.objects.filter(person=self.instance)
        else:
            self.fields['events'].queryset = Event.objects.none()

    sources = forms.ModelMultipleChoiceField(
        queryset = Source.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['type', 'date']
        widgets = {
            'type': forms.Select(choices=[
                ('birth', 'Birth'),
                ('death', 'Death'),
                ('life_event', 'Life Event'),
                ('marriage', 'Marriage')
            ]),
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'type', 'date', 'file_location']
        widgets = {
            'type': forms.Select(choices=[
                ('document', 'Document'),
                ('photo', 'Photo'),
                ('audio', 'Audio'),
                ('video', 'Video')
            ]),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'file_location': forms.FileInput()
        }