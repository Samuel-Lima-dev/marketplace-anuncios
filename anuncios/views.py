from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Anuncio
from .forms import CriarAnuncioForm


class AnunciosView(ListView):
    model = Anuncio
    template_name = 'anuncios.html'
    context_object_name = 'anuncios'

    def get_queryset(self):
        queryset = super().get_queryset()
        #Não retornar os anuncios do usuário logado 
        if self.request.user.is_authenticated:
            queryset = queryset.exclude(usuario=self.request.user)
        
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(titulo__icontains=search_query)

        return queryset

class DetalhesAnuncio(DetailView):
    model = Anuncio
    template_name = 'detalhes_anuncio.html'
    context_object_name = 'detalhes_anuncio'

class CriarAnuncioView(LoginRequiredMixin, CreateView):
    model = Anuncio
    form_class = CriarAnuncioForm
    template_name = 'formulario_anuncio.html'
    success_url = reverse_lazy('anuncios')
    login_url = 'login'

    def form_valid(self, form):
        # Vincular o anúncio ao usuario logado antes de salvar
        form.instance.usuario = self.request.user
        return super().form_valid(form)

        
class AtualizarAnuncioView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Anuncio
    form_class = CriarAnuncioForm
    template_name = 'atualizar_anuncio.html'
    login_url = 'login'

    #Garantir que apenas o criador do anuncio tenha acesso para modifica-lo
    def test_func(self):
        return self.get_object().usuario == self.request.user
    #Personalizar mensagem de erro
    #Redirecionar o usuario para página principal
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para editar o anuncio')
        return redirect('anuncios')

    def get_success_url(self):
        #Redirecionar para pagina de detalhes após à atualização
        return reverse('detalhes-anuncio', kwargs={'pk': self.object.pk})


class DeletarAnuncio(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Anuncio
    template_name = 'deletar_anuncio.html'
    success_url = reverse_lazy('anuncios')

    def test_func(self):
        return self.get_object().usuario == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, 'Você não tem permissão para deletar o anuncio')
    