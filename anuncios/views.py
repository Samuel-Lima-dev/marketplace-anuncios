from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Anuncio
from .form import CriarAnuncioForm



class Anunciosview(View):

    def get(self, request):
        anuncios = Anuncio.objects.all()

        search = request.GET.get('search')
        if search:
            anuncios = Anuncio.objects.filter(titulo__icontains=search)

        return render(
            request,
            'anuncios.html',
            {'anuncios': anuncios}
        )

class DetalhesAnuncio(View):

    def get(self, request, pk):
        anuncio = Anuncio.objects.get(pk=pk)

        return render(
            request,
            'detalhes_anuncio.html',
            {'detalhes_anuncio': anuncio}
        )


        
class CriarAnuncioView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        formulario_criacao = CriarAnuncioForm()

        return render(
            request,
            'formulario_anuncio.html',
            {'form_anuncio': formulario_criacao}
        )

    def post(self, request):
        novo_anuncio = CriarAnuncioForm(request.POST, request.FILES)

        if novo_anuncio.is_valid():
            anuncio = novo_anuncio.save(commit=False)
            anuncio.usuario = request.user
            anuncio.save()
            return redirect('anuncio')
        else:
            novo_anuncio = CriarAnuncioForm()

        return render(
            request,
            'formulario_anuncio.html',
            {'form_anuncio': novo_anuncio}
        )


class AtualizarAnuncioView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request, pk):
        anuncio = Anuncio.objects.get(pk=pk)
        formulario = CriarAnuncioForm(instance=anuncio)

        return render(
            request,
            'atualizar_anuncio.html',
            {'form_update': formulario}
        )

    def post(self, request, pk):
        anuncio = Anuncio.objects.get(pk=pk)
        formulario = CriarAnuncioForm(request.POST, request.FILES, instance=anuncio)

        if formulario.is_valid():
            formulario.save()
            return redirect('detalhes-anuncio', pk=pk)
        
        return render(
            request,
            'atualizar_anuncio.html',
            {'form_update': formulario}
        )

class DeletarAnuncio(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, requet, pk):
        anuncio = Anuncio.objects.get(pk=pk)
        return render(
            requet,
            'deletar_anuncio.html',
            {'anuncio': anuncio}
        )

    def post(self, request, pk):
        anuncio = Anuncio.objects.get(pk=pk)
        anuncio.delete()
        return redirect('anuncio')