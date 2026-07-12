from __future__ import annotations

from models.payment import Payment
from repositories.payment_repository import PaymentRepository


class PaymentManager:

    def __init__(self):

        self.repository = PaymentRepository()

    def create(
        self,
        activity_id: str,
        guild_id: int,
        channel_id: int,
        total: int,
        members: int,
        created_by: int
    ) -> Payment:

        payment = Payment()

        payment.activity_id = activity_id
        payment.guild_id = guild_id
        payment.channel_id = channel_id
        payment.total = total
        payment.each = total // members
        payment.created_by = created_by

        self.repository.save(payment)

        return payment

    def get(
        self,
        payment_id: str
    ):

        return self.repository.get(payment_id)

    def get_all(self):

        return self.repository.get_all()

    def update(
        self,
        payment: Payment
    ):

        self.repository.update(payment)

    def delete(
        self,
        payment_id: str
    ):

        self.repository.delete(payment_id)

    def mark_paid(
        self,
        payment: Payment,
        user_id: int
    ):

        if user_id not in payment.paid:

            payment.paid.append(user_id)

            self.update(payment)

    def reset(
        self,
        payment: Payment
    ):

        payment.paid.clear()

        self.update(payment)