from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from servise_msg.models import Mailing, Client


class TestStat(APITestCase):

    def test_mailing(self):
        mail_count = Mailing.objects.all().count()
        mail_create = {"start_mailing": now(),
                       "end_mailing": now(),
                       "text": "Test text",
                       "tags": "crazy",
                       "mobile_codes": '412'}
        response = self.client.post('http://127.0.0.1:8000/api/mailings/',
                                    mail_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mailing.objects.all().count(), mail_count + 1)
        self.assertEqual(response.data['text'], 'Test text')
        self.assertIsInstance(response.data['text'], str)

    def test_client(self):
        client_count = Client.objects.all().count()
        client_create = {"phone": "79999999999",
                         "code": "999",
                         "tag": "test_tag",
                         "time_zone": "UTC"}
        response = self.client.post('http://127.0.0.1:8000/api/clients/',
                                    client_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), client_count + 1)
        self.assertEqual(response.data['phone'], 79999999999)
        self.assertIsInstance(response.data['phone'], int)

    def test_message(self):
        response = self.client.get('http://127.0.0.1:8000/api/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stat(self):
        self.test_mailing()
        url = 'http://127.0.0.1:8000/api/mailings'
        response = self.client.get(f'{url}/1/info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'{url}/2/info/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(f'{url}/fullinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Общее количество рассылок'], 1)
        self.assertIsInstance(response.data['Общее количество рассылок'], int)
        self.assertIsInstance(
            response.data['Количество отправленных сообщений'],
            dict
        )
