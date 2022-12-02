from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from ckeditor.fields import RichTextField

class Accommodation(models.Model):
    name = models.CharField(max_length=50)
    location = models.TextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comments = models.ManyToManyField(
        User, through="Comment", related_name="comments_owned"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "name",
            "location",
        )
        ordering = ["-created_at"]   

    def __str__(self):
        return f"name: {self.name} | location: {self.location} | description: {self.description} | contact: {self.contact} | price: {self.price}"

class Comment(models.Model):
    text = models.TextField(
        validators=[
            MinLengthValidator(10, "El comentario debe tener como mínimo 10 caracteres")
        ]
    )
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        