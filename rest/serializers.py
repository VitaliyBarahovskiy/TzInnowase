from rest_framework import fields
from rest_framework.serializers import ModelSerializer
from rest.models import Ticket


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'title', 'desc', 'is_complete',)