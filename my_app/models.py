from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from ckeditor.fields import RichTextField


class Destino(models.Model):
    name = models.CharField(max_length=40)
    year = models.IntegerField()
    description = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='destino', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



    def __str__(self):
        return f"{self.name} - {self.year} - {self.description}"


class Comment(models.Model):
    text = models.TextField(
        validators=[
            MinLengthValidator(10, "El comentario debe tener como mínimo 10 caracteres")
        ]
    )
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        
