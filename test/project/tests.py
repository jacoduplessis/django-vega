from django.test import TestCase, SimpleTestCase
from project.models import Sale
import altair as alt
from django_vega import render, screenshot
from project.utils import generate_sales
import pathlib
import base64
import asyncio


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



class TestScreenshot(SimpleTestCase):

    def test_html_screenshot(self):
        asyncio.set_event_loop(
            asyncio.new_event_loop()
        )

        html = '<h1 style="color: red">Hallo, World</h1>'

        data = screenshot(html)

        pathlib.Path('html.png').write_bytes(base64.b64decode(data['png']))