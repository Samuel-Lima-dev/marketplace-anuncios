from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class Anuncio(models.Model):
    estado_produto = [
        ("Novo", "Novo"),
        ("Usado", "Usado"),
        ("Seminovo", "Seminovo")
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=100, choices=estado_produto, default='novo')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL , null=True)
    valor = models.FloatField()
    imagem = models.ImageField(upload_to="imagens/anuncios/")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

