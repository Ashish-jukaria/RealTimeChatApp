from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync
from .models import *
import json



class FirstConsumer(SyncConsumer):

    def websocket_connect(self,event):
        self.send({
            'type':'websocket.accept'
        })
        self.groupName=self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(self.groupName, self.channel_name)

        
    def websocket_receive(self,event):
        print('message recieved from client',event)
        async_to_sync(self.channel_layer.group_add)(self.groupName, self.channel_name)
        print(self.scope)
        if self.scope["user"].is_authenticated:
                async_to_sync(self.channel_layer.group_send)(
                    self.groupName,
                    {
                        "type": "chat.message",
                        "message": event['text'],
                    })
                group = Group.objects.get(group_name=self.groupName)
                data=json.loads(event['text'])
                chat_box=Chat(message=data['msg'],group=group)
                chat_box
                chat_box.save()
        else:
              self.send(json.dumps({
            'type':'websocket.send',
            'text':'User not Logged In'
        }))


    def chat_message(self,event):
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
     
    

    def websocket_disconnect(self,event):
        print("websocket_disconnected",event)