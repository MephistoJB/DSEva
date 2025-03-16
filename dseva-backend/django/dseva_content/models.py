import uuid
from django.db import models
from django.utils import timezone

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()
        
class Developer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    
class Repository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='', blank=True, )
    foreign_id = models.CharField(max_length=255, default='')
    type=models.CharField(max_length=255, default='Repository', editable=False)
    owner=models.ForeignKey(Developer, null=True, blank=True, related_name='repositories', on_delete=models.CASCADE)
    parent=models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.SET_NULL)
    #software
    watched_count=models.IntegerField(default=0)
    stars_count=models.IntegerField(default=0)
    loc = models.IntegerField(default=0)
    files = models.IntegerField(default=0)
    #contributors
    #sponsors
    #commits
    #pr
    created_at = AutoDateTimeField(default=timezone.now, editable=False)
    updated_at = AutoDateTimeField(default=timezone.now, editable=False)
    firstVisit = AutoDateTimeField(default=timezone.now, editable=False)
    lastVisit = AutoDateTimeField(default=timezone.now, editable=False)