import json
from channels.generic.websocket import WebsocketConsumer
from .models import Votes
from django.db.models import ObjectDoesNotExist


connectedConsumers = {}

'''
action: A | B | X | Y
'''


class MessagePayload:
    def __init__(self, action):
        self.action = action

    def to_json(self):
        return json.dumps({
            'action': self.action
        })

    @staticmethod
    def from_json(s):
        o = json.loads(s)
        if 'action' not in o:
            raise KeyError
        return MessagePayload(action=o['action'])

    def __str__(self):
        return "action: {}".format(self.action)


class VotesConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = self.scope['url_route']['kwargs']['room_id']

    def connect(self):
        if self.room_id not in connectedConsumers:
            connectedConsumers[self.room_id] = [self]
        else:
            connectedConsumers[self.room_id].append(self)
        self.accept()

        votes = Votes.objects.get_or_create(room_id=self.room_id)[0]
        self.send_votes_to_group(votes)

    def disconnect(self, close_code):
        connectedConsumers[self.room_id].remove(self)
        if len(connectedConsumers[self.room_id]) == 0:
            del connectedConsumers[self.room_id]

    def receive(self, **kwargs):
        try:
            message = MessagePayload.from_json(kwargs['text_data'])
        except (KeyError, json.decoder.JSONDecodeError):
            return

        if message.action == 'RESET':
            try:
                votes = Votes.objects.get(room_id=self.room_id)
            except ObjectDoesNotExist:
                return
            votes.A = 0
            votes.B = 0
            votes.X = 0
            votes.Y = 0
        else:
            votes = Votes.objects.get_or_create(room_id=self.room_id)[0]

            if message.action == 'A':
                votes.A += 1
            elif message.action == 'B':
                votes.B += 1
            elif message.action == 'X':
                votes.X += 1
            elif message.action == 'Y':
                votes.Y += 1
            else:
                return

        votes.save()
        self.send_votes_to_group(votes)

    def send_votes_to_group(self, votes: Votes):
        votes_json_str = json.dumps({
            'A': votes.A,
            'B': votes.B,
            'X': votes.X,
            'Y': votes.Y,
        })

        for consumer in connectedConsumers[self.room_id]:
            consumer.send(text_data=votes_json_str)


