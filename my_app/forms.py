from ckeditor.widgets import CKEditorWidget
from django import forms

from my_app.models import Viaje


class ViajeForm(forms.ModelForm):
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


    class Meta:
        model = Viaje
        fields = ["name", "year", "description"]