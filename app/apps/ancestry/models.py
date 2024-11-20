from django.db import models
from django.utils.timezone import now

class Tree(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)
    file_location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Person(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.DO_NOTHING, related_name='members')
    name = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    sources = models.ManyToManyField(Source, blank=True)

    father = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_as_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_as_mother')

    def __str__(self):
        return self.name

    def siblings(self):
        return Person.objects.filter(
            models.Q(father=self.father) | models.Q(mother=self.mother)
        ).exclude(id=self.id)

    def children(self):
        return self.children_as_father.all() | self.children_as_mother.all()

class Event(models.Model):
    type = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True, null=True, related_name='events')

    def __str__(self):
        return f'{self.type}: {self.date}'