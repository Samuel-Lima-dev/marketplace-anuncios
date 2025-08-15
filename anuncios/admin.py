from django.contrib import admin
from .models import Categoria, Anuncio


@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ["titulo", "descricao", "categoria", "valor", "estado", "imagem", "data"]
    
    
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome"]