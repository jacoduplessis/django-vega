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

## server rendering

Server rendering to svg and png is done with headless chromium. Ensure your system has a recent version installed.
Depending on your expected workload, you will either want to keep a browser process running in the background, or
start a short-lived instance for each render.

The `render` function will return both an SVG string and a base64-encoded PNG.

Should a headless chromium instance be spawned, pass a path to the executable via the `spawn` argument. The alternative
is to have a running instance at port 9222.

```python

import base64
from django_vega import render


spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v3.json",
  "description": "A simple bar chart with embedded data.",
  "data": {
    "values": [
      {"a": "A","b": 28}, {"a": "B","b": 55}, {"a": "C","b": 43},
      {"a": "D","b": 91}, {"a": "E","b": 81}, {"a": "F","b": 53},
      {"a": "G","b": 19}, {"a": "H","b": 87}, {"a": "I","b": 52}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "a", "type": "ordinal"},
    "y": {"field": "b", "type": "quantitative"}
  }
}

result = render(spec, spawn='/Applications/Chromium.app/Contents/MacOS/Chromium')

with open('image.png', 'wb') as f:
    b = base64.b64decode(result['png'])
    f.write(b)

with open('image.svg', 'w') as f:
    f.write(result['svg'])



```

## testing

A test Django application is located in the `test` folder.

Automated testing is on the todo list.

## todo

- allow for multiple versions of vega, vega-lite and vega-embed in rendering
- set background color during render
- regression ([example](https://altair-viz.github.io/gallery/poly_fit.html), [lib](https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.polynomial.Polynomial.fit.html))
