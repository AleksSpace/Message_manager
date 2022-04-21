from rest_framework import serializers

from servise_msg.models import Client, Mailing, Message


class MailingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для рассылки
    """
    class Meta:
        model = Mailing
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для клиентов
    """
    class Meta:
        model = Client
        fields = ('phone', 'code', 'tag', 'time_zone')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
