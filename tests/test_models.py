from django.utils.timezone import now
from rest_framework.test import APITestCase

from servise_msg.models import Mailing, Client, Message


class TestModel(APITestCase):

    def test_creates_mailings(self):
        mailing = Mailing.objects.create(start_mailing=now(),
                                         end_mailing=now(),
                                         text='Simple text',
                                         tags='test_tag',
                                         )
        self.assertIsInstance(mailing, Mailing)
        self.assertEqual(mailing.tags, 'test_tag')

    def test_creates_clients(self):
        client = Client.objects.create(phone='71234567890',
                                       code='123',
                                       tag='test_tag',
                                       time_zone='UTC')
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone, '71234567890')

    def test_creates_messages(self):
        self.test_creates_mailings()
        self.test_creates_clients()
        message = Message.objects.create(status='No sent',
                                         mailing_id=1,
                                         client_id=1)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.status, 'No sent')
