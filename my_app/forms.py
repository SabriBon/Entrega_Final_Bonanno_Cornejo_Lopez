from ckeditor.widgets import CKEditorWidget
from django import forms

from my_app.models import Destino


class DestinoForm(forms.ModelForm):
    name = forms.CharField(
        label="Lugar de destino",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "my_app-name",
                "placeholder": "Lugar de destino",
                "required": "True",
            }
        ),
    )
    year = forms.IntegerField(
        label="Año",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "my_app-year",
                "placeholder": "Año de viaje",
                "required": "True",
            }
        ),
    )

    description = forms.CharField(
        label="Comentarios:",
        required=False,
        widget=CKEditorWidget(
            attrs={
                "class": "my_app-description",
                "placeholder": "Envianos tu comentario",
                "required": "True",
            }
        ),
    )

    image = forms.ImageField()


    class Meta:
        model = Destino
        fields = ["name", "year", "description", "image"]

class CommentForm(forms.Form):
    comment_text = forms.CharField(
        label="",
        required=False,
        max_length=500,
        min_length=10,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "class": "comment-text",
                "placeholder": "Ingrese su comentario...",
                "required": "True",
                "max_length": 500,
                "min_length": 10,
                "rows": 2,
                "cols": 10,
                "style":"min-width: 100%",
            }
        ),
    )

