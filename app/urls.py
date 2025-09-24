from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from anuncios.views import *
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    
    path('anuncios/', AnunciosView.as_view(), name='anuncios'),
    path('meus_anuncios/', MeusAnuncios.as_view(), name='meus_anuncios'),
    path('criar-anuncio/', CriarAnuncioView.as_view(), name='criar-anuncio'),
    path('detalhes/<int:pk>/', DetalhesAnuncio.as_view(), name='detalhes-anuncio'),
    path('atualizar/<int:pk>/', AtualizarAnuncioView.as_view(), name='atualizar-anuncio-form' ),
    path('exluir/<int:pk>/', DeletarAnuncio.as_view(), name='excluir_anuncio'),

    path('cadastro/pessoa-fisica/', CreateNaturalUserView.as_view(), name='cadastro-pessoa-fisica'),
    path('cadastro/pessoa-juridica/', CreateLegalPersonUserView.as_view(), name='cadastro-pessoa-juridica'),
    path('login/', AuthenticationFormUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
