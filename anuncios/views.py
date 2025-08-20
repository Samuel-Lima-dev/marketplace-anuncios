from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Anuncio
from .form import CriarAnuncioForm



class Anunciosview(ListView):

    model = Anuncio
    template_name = 'anuncios.html'
    context_object_name = 'anuncios'


    def get_queryset(self):
        queryset = super().get_queryset().filter()
    
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

        
class AtualizarAnuncioView(LoginRequiredMixin, UpdateView):
    model = Anuncio
    form_class = CriarAnuncioForm
    template_name = 'atualizar_anuncio.html'
    login_url = 'login'

    def get_success_url(self):
        #Redirecionar para pagina de detalhes após à atualização
        return reverse('detalhes-anuncio', kwargs={'pk': self.object.pk})


class DeletarAnuncio(LoginRequiredMixin, DeleteView):
    model = Anuncio
    template_name = 'deletar_anuncio.html'
    success_url = reverse_lazy('anuncios')
    