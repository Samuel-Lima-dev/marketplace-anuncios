from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import models
from .models import ChatRoom, Message
from anuncios.models import Anuncio

@login_required
def chat_room_view(request, anuncio_id):
    ''' Criar ou buscar uma nova sala de chat '''
    anuncio = get_object_or_404(Anuncio, pk=anuncio_id)
    seller = anuncio.usuario
    buyer = request.user

    if buyer == seller:
       raise PermissionDenied('Você não pode iniciar uma conversa consigo mesmo')

    chat_room, created = ChatRoom.objects.get_or_create(
        product=anuncio,
        seller=seller,
        buyer=buyer
    )
    #Redirecionar paga pagina de bate papo
    return redirect('chat_room', room_id=chat_room.pk)

@login_required
def chat_list(request):
    '''Listar Todas as conversas'''
    conversa = ChatRoom.objects.filter(
        models.Q(buyer=request.user) | models.Q(seller=request.user)
    ).select_related('product', 'seller', 'buyer')

    return render(
        request,
        'chat_list.html',
        {'rooms': conversa}
    )

@login_required
def chat_room(request, room_id):
    '''Renderiza a página da sala de chat.'''
    chat_room = get_object_or_404(ChatRoom, pk=room_id)
    #Verificar se o usuario pertence a sala de chat (comprador ou vendedor)
    if request.user != chat_room.buyer and request.user != chat_room.seller:
        raise PermissionDenied('Você não tem permissão para acessar esta sala')

    #pegar historico de mensagem do usuario
    message = Message.objects.filter(chat_room=chat_room).order_by('sent_at')

    return render(
        request, 
        'chat_room.html', 
        {
            'room_id': room_id,
            'chat_room': chat_room,
            'message': message
        }
    )