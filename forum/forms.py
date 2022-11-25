from ckeditor.widgets import CKEditorWidget
from django import forms

from forum.models import Forum


class ForumForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre del Usuario",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "forum-name",
                "placeholder": "Ingrese su nombre",
                "required": "True",
            }
        ),
    )
    email = forms.CharField(
        label="Email del Usuario",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "forum-location",
                "placeholder": "Ingrese su Email",
                "required": "True",
            }
        ),
    )
    
    contact = forms.CharField(
        label="Teléfono de contacto",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "forum-contact",
                "placeholder": "Ingrese un número ",
                "required": "False",
            }
        ),
    )
    description = forms.CharField(
        label="Agregue su Reseña",
        required=False,
        widget=CKEditorWidget(
            attrs={
                "class": "forum-description",
                "placeholder": "Contanos tu experiencia del Viaje",
                "required": "True",
            }
        ),
    )

    
    class Meta:
        model = Forum
        fields = ["name", "contact", 'email', "description",  ]