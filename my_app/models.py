from django.db import models
from ckeditor.fields import RichTextField


class Viaje(models.Model):
    name = models.CharField(max_length=40)
    year = models.IntegerField()
    description = RichTextField(null=True, blank=True)



    def __str__(self):
        return f"{self.name} - {self.year} - {self.description}"



