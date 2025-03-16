import uuid
from django.db import models # type: ignore
from django.utils import timezone # type: ignore
#from dseva_content.models.repository import Repository

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()
    
class Developer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foreign_id = models.CharField(max_length=255, unique=True, blank=True, null=True) 
    name = models.CharField(max_length=255)
    repository = models.ForeignKey('dseva_content.Repository', null=True, blank=True, related_name='owner', on_delete=models.CASCADE)
    #contributions = models.ForeignKey(Repository, null=True, blank=True, related_name='contributor', on_delete=models.CASCADE)
    #watched = models.ForeignKey(Repository, null=True, blank=True, related_name='watcher', on_delete=models.CASCADE)
    #starred = models.ForeignKey(Repository, null=True, blank=True, related_name='starrer', on_delete=models.CASCADE)
    #subscription = models.ForeignKey(Repository, null=True, blank=True, related_name='subscriber', on_delete=models.CASCADE)
    follow=models.ForeignKey('self', null=True, blank=True, related_name='follower', on_delete=models.CASCADE)
    new = models.BooleanField(default=True)
    created_at = AutoDateTimeField(default=timezone.now, editable=False)
    updated_at = AutoDateTimeField(default=timezone.now, editable=False)
    firstVisit = AutoDateTimeField(default=timezone.now, editable=False)
    lastVisit = AutoDateTimeField(default=timezone.now, editable=False)
    type = models.CharField(max_length=255, default="Developer", editable=False)