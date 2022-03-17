from django.db import models

class UploadImage(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")