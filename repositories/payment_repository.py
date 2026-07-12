from __future__ import annotations

from core.constants import PAYMENTS_FILE
from models.payment import Payment
from storage.json_storage import JsonStorage


class PaymentRepository:

    def __init__(self):

        self.storage = JsonStorage(
            PAYMENTS_FILE
        )

    def save(
        self,
        payment: Payment
    ):

        data = self.storage.load()

        data.setdefault(
            "payments",
            {}
        )

        data["payments"][payment.id] = (
            payment.to_dict()
        )

        self.storage.save(data)

    def update(
        self,
        payment: Payment
    ):

        self.save(payment)

    def get(
        self,
        payment_id: str
    ):

        data = self.storage.load()

        payment = data.get(
            "payments",
            {}
        ).get(payment_id)

        if payment is None:

            return None

        return Payment.from_dict(
            payment
        )

    def get_all(self):

        data = self.storage.load()

        payments = []

        for payment in data.get(
            "payments",
            {}
        ).values():

            payments.append(
                Payment.from_dict(payment)
            )

        return payments

    def delete(
        self,
        payment_id: str
    ):

        data = self.storage.load()

        if payment_id in data.get(
            "payments",
            {}
        ):

            del data["payments"][payment_id]

        self.storage.save(data)