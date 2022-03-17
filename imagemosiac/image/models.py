from django.db import models
from uuid import uuid4

def imageuuid(instance,filename):
    return f"images/{uuid4()}.{filename.split('.')[-1]}"

class UploadImage(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=imageuuid)