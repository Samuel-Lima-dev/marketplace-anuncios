from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from .forms import NaturalPersonForm, LegalPersonForm


#Cadastro de pessoa fisica
class CreateNaturalUserView(View):
    
    def get(self, request):
        form = NaturalPersonForm()
        return render(
            request,
            'create_natural_person.html',
            {'form': form}
        )

    def post(self, request):
        
        form = NaturalPersonForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anuncios')
        else:
            return render(
                request,
                'create_natural_person.html',
                {'form': form}
            )
        

#Cadstro de pessoa juridica
class CreateLegalPersonUserView(View):

    def get(self, request):
        form = LegalPersonForm()
        return render(
            request,
            'create_legal_person.html',
            {'form': form}
        )  

    def post(self, request):
        form = LegalPersonForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('anuncios')
        else:
            return render(
                request,
                'create_natural_person.html',
                {'form': form}
            )

#Login
class AuthenticationFormUserView(View):

    def get(self, request):
        form = AuthenticationForm()
        return render(
            request,
            'login.html',
            {'form': form}
        )

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('anuncios')
        else:
            form = AuthenticationForm()
            return render(
                request,
                'login.html',
                {'form': form}
            )

def logout_view(request):
    logout(request)
    return redirect('anuncios')