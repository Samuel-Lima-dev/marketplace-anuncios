from django.db import models
from accounts.models import User

#Sala de bate papo
class ChatRoom(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller') 
    product = models.ForeignKey('anuncios.Anuncio', on_delete=models.CASCADE, related_name='product')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Garantir que só exista uma conversa entre um comprador e vendedor especifico
        constraints = [
            models.UniqueConstraint(fields=['buyer', 'seller', 'product'], name='unique_chat_room')
        ]
    
    def __str__(self):
        return f"Conversa entre {self.buyer} e {self.seller} - {self.product}"
    
class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_room')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('sent_at',)

    def __str__(self):
        return self.sender.username