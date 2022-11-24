from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.forms import FloatField, IntegerField

class Accommodation(models.Model):
    name = models.CharField(max_length=50)
    location = models.TextField()
    description = RichTextField(null=True, blank=True)
    contact = IntegerField()
    price = FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"name: {self.name} | location: {self.location} | description: {self.description} | contact: {self.contact} | price: {self.price}"