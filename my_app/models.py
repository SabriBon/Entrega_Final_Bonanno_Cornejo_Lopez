from django.contrib.auth.models import User

from django.db import models
from ckeditor.fields import RichTextField


class Destino(models.Model):
    name = models.CharField(max_length=40)
    year = models.IntegerField()
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='destino', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    def __str__(self):
        return f"{self.name} - {self.year} - {self.description}"



