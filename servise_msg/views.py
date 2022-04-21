from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """
        Сводные данные по конкретной рассылке
        """
        queryset = Mailing.objects.all()
        mailing = get_object_or_404(queryset, pk=pk)
        serializer = MailingSerializer(mailing)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullinfo(self, request):
        """
        Сводные данные по всем рассылкам
        """
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Общее количество рассылок': total_count,
                   'Количество отправленных сообщений': ''}
        result = {}
        for row in mailing:
            res = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            group_sent = mail.filter(status='Sent').count()
            group_no_sent = mail.filter(status='No sent').count()
            res['Total messages'] = len(mail)
            res['Sent'] = group_sent
            res['No sent'] = group_no_sent
            result[row['id']] = res
        content['Количество отправленных сообщений'] = result
        return Response(content)
