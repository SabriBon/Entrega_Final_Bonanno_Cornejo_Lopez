from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Accommodation(models.Model):
    name = models.CharField(max_length=50)
    location = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"name: {self.name} | location: {self.location} | description: {self.description} | contact: {self.contact} | price: {self.price}"