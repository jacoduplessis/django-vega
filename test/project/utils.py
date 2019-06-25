from .models import Sale
import random
from datetime import timedelta, datetime
from django.utils.timezone import make_aware, utc


def generate_sales():
    random.seed(99)
    base_date = make_aware(datetime(year=2019, month=6, day=5), timezone=utc)

    sales = []
    for i in range(1000):
        minutes = random.randint(500, 5000)
        amount = random.randint(500, 5000)
        payment_method = random.choice(Sale.PAYMENT_METHOD_CHOICES)[0]
        date = base_date - timedelta(minutes=minutes)
        sales.append(
            Sale(date=date, amount=amount, payment_method=payment_method)
        )

    Sale.objects.bulk_create(sales)
    return sales
