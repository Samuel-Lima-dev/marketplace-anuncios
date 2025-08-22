from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout


class CriarUsuarioView(View):

    def get(self, request):
        formulario_cadastro = UserCreationForm()

        return render(
            request,
            'cadastro_usuario.html',
            {'form': formulario_cadastro}
        )
    
    def post(self, request):
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            login(request, usuario) 
            return redirect('anuncios')
        
        return render(
            request,
            'cadastro_usuario.html',
            {'form': formulario}
        )
    
class LoginUsuarioView(View):

    def get(self, request):
        formulario_login = AuthenticationForm()

        return render(
            request,
            'login.html',
            {'form_login': formulario_login}
        )
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        usuario = authenticate(request, username = username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('anuncios')
        else:
            formulario_login = AuthenticationForm()
            return render(
                request, 
                'login.html',
                {'form_login': formulario_login}

            )

def logout_usuario(request):
    logout(request)
    return redirect('anuncios')