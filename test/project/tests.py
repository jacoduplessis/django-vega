from django.test import TestCase
from project.models import Sale
import altair as alt
from django_vega import render
from project.utils import generate_sales
import datetime
import json
import pathlib
import base64


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super().default(obj)


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

        output = render(chart.to_json(cls=JSONEncoder))

        pathlib.Path('test_2.svg').write_text(output['svg'])
        pathlib.Path('test_2.png').write_bytes(base64.b64decode(output['png']))


