from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
from asyncio import sleep
from channels.exceptions import StopConsumer

# This works with producer
#

# Ca sa suporte alti clienti imi trebuie (alte instante de websocket). Imi trebuie channel layers. 
# Channel layers is a "first in first out" data structure. 
# Is a queue of messages that this data structure receive from the clients.
# For every message on the channel in this Queue, django will call the asigned consumer
# In my case for each message in the channel, Django will call the WSConsumer class.
# So... to use the channel layer I have to use Redis (the inmemory database)  

class WSConsumer(AsyncWebsocketConsumer):
    group_name = "dashboard"
    
    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        print("Client is connected!")
        # print(self.scope) # important details about the client
        
    
    
    async def disconnect(self, close_code):
        print('disconnected! ', close_code)
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()

    ######## OPTIONAL IN THIS CASE #########
    # to receive data from client
    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        val = datapoint['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'deprocessing',
                'message': val
            }
        )
        #print(text_data)

    async def deprocessing(self, event):
        # Receive message from client and send to group
        valOther = event['message']
        await self.send(json.dumps({'message': valOther}))