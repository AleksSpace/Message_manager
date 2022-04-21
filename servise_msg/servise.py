from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from servise_msg.mailing import send_message
from servise_msg.models import Client, Mailing, Message


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(
            Q(mobile_code=mailing.mobile_codes) | Q(tag=mailing.tags)
        ).all()
        for client in clients:
            Message.objects.create(
                status="No sent",
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(mailing_id=instance.id,
                                             client_id=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone,
                "text": mailing.text
            }
            client_id = client.id
            mailing_id = mailing.id
            if instance.to_send:
                send_message.apply_async((data, client_id, mailing_id),
                                         expires=mailing.end_mailing)
            else:
                send_message.apply_async((data, client_id, mailing_id),
                                         eta=mailing.start_mailing,
                                         expires=mailing.end_mailing)
