from urllib.request import urlretrieve
import shutil
from pathlib import Path

paths = [
    'vega/build/vega.js',
    'vega/build/vega.min.js',
    'vega-lite/build/vega-lite.js',
    'vega-lite/build/vega-lite.min.js',
    'vega-embed/build/vega-embed.js',
    'vega-embed/build/vega-embed.min.js',
]

for path in paths:

    name = Path(path).name

    url = f'https://unpkg.com/{path}'
    fp, _ = urlretrieve(url)
    dst = f'./django_vega/static/django_vega/{name}'
    shutil.move(fp, dst)
