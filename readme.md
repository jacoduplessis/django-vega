# django-vega

## install

```
pip install django-vega
```

## usage

```python
from django_vega.views import AltairTemplateView
from .models import Sale
import altair as alt


class SaleView(AltairTemplateView):
    queryset = Sale.objects.all().values('date', 'amount', 'payment_method')
    chart_title = 'All Sales'
    embed_options = {
        'renderer': 'svg'
    }

    def get_chart(self):
        return alt.Chart(self.get_data()).mark_circle().encode(
            x='date:T',
            y='amount:Q',
            color='payment_method:N'
        )
```

## testing

A test Django application is located in the `test` folder.

Automated testing is on the todo list.
