from ckeditor.widgets import CKEditorWidget
from django import forms

from accommodation.models import Accommodation


class AccommodationForm(forms.ModelForm):
    name = forms.CharField(
        label="Nombre del alojamiento",
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "accommodation-name",
                "placeholder": "Ingrese el nombre",
                "required": "True",
            }
        ),
    )
    location = forms.CharField(
        label="Ubicación del alojamiento",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "accommodation-location",
                "placeholder": "Ingrese la ubicación",
                "required": "True",
            }
        ),
    )
    
    contact = forms.CharField(
        label="Teléfono de contacto",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "accommodation-contact",
                "placeholder": "Ingrese un número",
            }
        ),
    )
    price = forms.CharField(
        label="Precio",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "accommodation-price",
                "placeholder": "Ingrese precio por noche ",
            }
        ),
    )

    description = forms.CharField(
        label="Descripción:",
        required=False,
        widget=CKEditorWidget(
            attrs={
                "class": "accommodation-description",
                "placeholder": "su opinión nos interesa",
                "required": "True",
            }
        ),
    )

    
    class Meta:
        model = Accommodation
        fields = ["name", "location", "contact", "price", "description" ]
