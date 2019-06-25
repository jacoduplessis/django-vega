from django.test import TestCase
from project.models import Sale
import altair as alt
from django_vega import render
from project.utils import generate_sales
import pathlib
import base64


class TestSimpleChart(TestCase):

    @classmethod
    def setUpTestData(cls):
        generate_sales()

    def test_chart(self):
        qs = Sale.objects.all().values('date', 'amount', 'payment_method')

        data = alt.Data(values=list(qs))

        chart = alt.Chart(data).mark_bar().encode(
            x='date:T',
            y='amount:Q',
            color='payment_method:N',
            column='payment_method:N'
        )

        output = render(chart.to_dict())

        pathlib.Path('test.svg').write_text(output['svg'])
        pathlib.Path('test.png').write_bytes(base64.b64decode(output['png']))
