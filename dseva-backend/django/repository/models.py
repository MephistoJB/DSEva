import uuid

from django.db import models

class Repository1(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
<<<<<<< HEAD
=======

class Developer1(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
>>>>>>> 098b29c (Enabled remote debugging and github sync of the first objects)
