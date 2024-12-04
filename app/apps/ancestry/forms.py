from django import forms
from .models import Tree, Person, Event, Source

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'birth_date', 'death_date', 'mother', 'father']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tree:
            tree_members = Person.objects.filter(tree=self.instance.tree).exclude(id=self.instance.id)
            self.fields['mother'].queryset = tree_members
            self.fields['father'].queryset = tree_members