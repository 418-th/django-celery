from mailer.tasks import send_email_notifications
from elk.utils.testing import TestCase, create_customer
import logging

logger = logging.getLogger(__name__)


class TestSendEmailNotifications(TestCase):

    def test_send_email_has_no_errors(self):
        customers_data = []
        for x in range(10):
            customer = create_customer()
            customers_data.append(
                {
                    'customer_email': customer.customer_email,
                    'customer_first_name': customer.customer_first_name,
                    'customer_last_name': customer.customer_last_name,
                    'native_language': customer.native_language,
                }
            )

        send_email_notifications()
        send_email_notifications(customers_data=customers_data)
