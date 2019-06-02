from django.db import models


class Sale(models.Model):

    CREDIT_CARD = 'credit_card'
    CASH = 'cash'
    BITCOIN = 'bitcoin'

    PAYMENT_METHOD_CHOICES = (
        (CREDIT_CARD, 'Credit Card'),
        (CASH, 'Cash'),
        (BITCOIN, 'Bitcoin'),
    )

    date = models.DateTimeField()
    amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
