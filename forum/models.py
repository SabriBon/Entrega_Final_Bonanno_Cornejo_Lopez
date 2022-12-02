from django.db import models
from ckeditor.fields import RichTextField


class Forum(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    contact = models.IntegerField()
    description = RichTextField(null=True, blank=True)



def __str__(self):
    return f"{self.name} - {self.email} - {self.contact} - {self.description}"

