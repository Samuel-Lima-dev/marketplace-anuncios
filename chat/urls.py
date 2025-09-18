from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.chat_list, name='chat_list'),
    path("<int:anuncio_id>/", views.chat_room_view, name="start_chat"),
    path('sala/<int:room_id>/', views.chat_room, name='chat_room')
]
