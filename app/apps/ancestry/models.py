from django.db import models
from django.utils.timezone import now

class Tree(models.Model):
    created_date = models.DateTimeField(default=now, editable=False)

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Source(models.Model):
    AUDIO = 'AUDIO'
    DOCUMENT = 'DOCUMENT'
    PHOTO = 'PHOTO'
    VIDEO = 'VIDEO'

    SOURCE_TYPES = (
        (AUDIO, 'audio'),
        (DOCUMENT, 'document'),
        (PHOTO, 'photo'),
        (VIDEO, 'video'),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=SOURCE_TYPES)
    date = models.DateField(null=True, blank=True)
    file_location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.name} ({self.type}): {self.date}'

class Event(models.Model):
    BIRTH = 'BIRTH'
    DEATH = 'DEATH'
    OTHER = 'OTHER'

    EVENT_TYPES = (
        (BIRTH, 'birth'),
        (DEATH, 'death'),
        (OTHER, 'other'),
    )

    type = models.CharField(max_length=200, choices=EVENT_TYPES)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.type}: {self.date}'

class Person(models.Model):
    created_date = models.DateTimeField(default=now, editable=False)

    tree = models.ForeignKey(Tree, on_delete=models.DO_NOTHING, related_name='members')
    name = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    father = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_as_father')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children_as_mother')

    events = models.ManyToManyField(Event, blank=True)
    sources = models.ManyToManyField(Source, blank=True)

    def __str__(self):
        return self.name