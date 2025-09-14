import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User
from anuncios.models import Anuncio
from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']

        self.room_group_name = f'Chat_{self.room_id}'

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.disconnect(403)

    #Sair do grupo da sala
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name  
        )

    async def receive(self, text_data):

        text_data = json.loads(text_data)
        message_text = text_data['message']

        #salvar mensagem no banco de dados
        new_message = await self.save_message(message_text)

        #enviando mensagem para o prupo da sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': new_message.content,
                'sender': self.user.username,
                'sent_at': new_message.sent_at.strftime('%d/%m/%Y %H:%M')
            }
        )

    #Receber a mensagem do grupo da sala
    async def chat_message(self, event):
        message=event['message']
        sender=event['sender']
        sent_at = event['sent_at']

        #Envia a mensagem de volta para o cliente
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'sent_at':sent_at
        }))

    @database_sync_to_async
    def save_message(self, message_content):
        
        chat_room = ChatRoom.objects.get(pk=self.room_id)
        
        message = Message.objects.create(
            chat_room = chat_room,
            sender=self.user,
            content=message_content
        )
        return message
