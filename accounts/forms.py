from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        #Definindo o username a partir do email
        user.username = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class NaturalPersonForm(CustomUserForm):
    name = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=11)
    date_birth = forms.DateField()

    #Herda o Meta do CustomUserForm e adiciona os novos campos 
    class Meta(CustomUserForm.Meta):
        fields = ['name', 'cpf', 'email', 'date_birth', 'password1', 'password2']

    #Garante que tudo funcione, caso contrario, nada será salvo
    @transaction.atomic 
    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            NaturalPerson.objects.create(
                user = user,
                name = self.cleaned_data['name'],
                cpf = self.cleaned_data['cpf'],
                date_birth = self.cleaned_data['date_birth']
            )
        return user
        
class LegalPersonForm(CustomUserForm):
    name = forms.CharField(max_length=100)
    cnpj = forms.CharField(max_length=14)

    class Meta(CustomUserForm.Meta):
        fields = ('name', 'cnpj', 'email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            LegalPerson.objects.create(
                user =user,
                name = self.cleaned_data['name'],
                cnpj = self.cleaned_data['cnpj']
            )
        
        return user


    