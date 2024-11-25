from django.db import models

# Create your models here.
class Document_sphinx(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')