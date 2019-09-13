from urllib.request import urlretrieve
import shutil
from pathlib import Path

paths = [
    'vega@5/build/vega.js',
    'vega@5/build/vega.min.js',
    'vega-lite@3/build/vega-lite.js',
    'vega-lite@3/build/vega-lite.min.js',
    'vega-embed@5/build/vega-embed.js',
    'vega-embed@5/build/vega-embed.min.js',
]

for path in paths:

    name = Path(path).name

    url = f'https://unpkg.com/{path}'
    fp, _ = urlretrieve(url)
    dst = f'./django_vega/static/django_vega/{name}'
    shutil.move(fp, dst)
