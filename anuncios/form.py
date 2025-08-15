from django.forms import ModelForm
from .models import Anuncio


class CriarAnuncioForm(ModelForm):

    class Meta:
        model = Anuncio
        exclude = ["usuario"]