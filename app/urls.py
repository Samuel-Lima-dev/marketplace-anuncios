from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from anuncios.views import Anunciosview, CriarAnuncioView, DetalhesAnuncio, AtualizarAnuncioView, DeletarAnuncio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anuncio/', Anunciosview.as_view(), name='anuncio'),
    path('criar-anuncio/', CriarAnuncioView.as_view(), name='criar-anuncio'),
    path('detalhes/<int:pk>/', DetalhesAnuncio.as_view(), name='detalhes-anuncio'),
    path('atualizar/<int:pk>/', AtualizarAnuncioView.as_view(), name='atualizar-anuncio-form' ),
    path('exluir/<int:pk>/', DeletarAnuncio.as_view(), name='excluir_anuncio')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
