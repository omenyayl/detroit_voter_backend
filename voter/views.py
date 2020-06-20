from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from .models import Votes
from django.db import models


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def home(request):
    content = {
        'hello': 'world'
    }
    return Response(content)


@api_view(['DELETE'])
@renderer_classes([JSONRenderer])
def delete_room(request, room_id):
    try:
        votes = Votes.objects.get(room_id=room_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    votes.delete()

    return Response(status=status.HTTP_200_OK)
