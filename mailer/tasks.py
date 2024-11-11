from typing import List, Dict, Any

from datetime import timedelta
from django.utils import timezone

from elk.celery_app import app as celery_app


@celery_app.task(bind=True, max_retries=5)
def send_email_notifications(self, customers_data: List[Dict[str, Any]] = None):
    from mailer.owl import Owl
    from crm.models import Customer

    try:
        index = 0

        if customers_data is None:
            timezone_now = timezone.now()

            customers_data: List[Dict[str]] = list(
                Customer.objects.filter(
                    classes__subscription__isnull=False,
                    classes__timeline__end__lt=timezone_now - timedelta(weeks=1),
                    classes__is_fully_used=False,
                ).values(
                    'customer_email',
                    'customer_first_name',
                    'customer_last_name',
                    'native_language',
                ).distinct()
            )  # list() is required to serialize object to next worker, if this fails
        for index, customer in enumerate(customers_data):
            owl_instance = Owl(
                template='mail/class/student/scheduled.html',
                ctx={
                    'first_name': customer.get('customer_first_name'),
                    'last_name': customer.get('customer_last_name'),
                    'language': customer.get('native_language')
                },
                to=[customer.get('customer_email')],
            )
            owl_instance.send()

    except Exception as exc:
        self.retry(exc=exc, customers_data=customers_data[index::])


@celery_app.task
def send_email(owl):
    owl.msg.send()
