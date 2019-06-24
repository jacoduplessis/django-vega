from .browser import Browser
import asyncio
from string import Template
import json
import subprocess
from typing import Dict
import logging
from pathlib import Path

logger = logging.getLogger()

expression = Template("""
        
        var spec = $spec;
        var scaleFactor = $scale;
        
        vegaEmbed('#viz', spec, {})    
        
        new Promise((resolve, reject) => {
        
            const response = {}
        
            const view = new vega.View(vega.parse(vl.compile(spec).spec), {
              loader: vega.loader(),
              logLevel: vega.Warn,
              renderer: 'none',
            })
            .initialize()

            p1 = view.toCanvas(scaleFactor)
            .then(canvas => {
                response['png'] = canvas.toDataURL('image/png').slice(22)  
            })
            
            p2 = view.toSVG(scaleFactor)
            .then(svg => {
                response['svg'] = svg
            })
            
            Promise.all([p1, p2]).then(() => {
                resolve(JSON.stringify(response))
            })            
                    
        })
        
        
            
        """)


def html_content():
    return Template("""
<!DOCTYPE html>
<html>
<head>
  <title>Embedding Vega-Lite</title>
  <script>$vega</script>
  <script>$vega_lite</script>
  <script>$vega_embed</script>
</head>
<body>
  <div id="viz"></div>
</body>
</html>
""").substitute(**get_libs())


def get_libs():
    return {
        'vega': (Path(__file__).parent / 'static' / 'django_vega' / 'vega.js').read_text(),
        'vega_lite': (Path(__file__).parent / 'static' / 'django_vega' / 'vega-lite.js').read_text(),
        'vega_embed': (Path(__file__).parent / 'static' / 'django_vega' / 'vega-embed.js').read_text(),
    }


def render(vega_spec: Dict, scale: int = 1, browser: Browser = None, spawn: str = None) -> Dict[str, str]:
    """

    :param vega_spec: Vega specfication to render, as dict
    :param scale: Scale to use for rendering
    :param browser: django_vega.browser.Browser instance to use
    :param spawn: Path to chrome/chromium executable, will spawn process if provided
    :return: Dictionary with 'svg' => svg string, 'png' => base64 png
    """

    must_close_browser = False

    if spawn:
        proc = subprocess.Popen([
            spawn,
            '--headless',
            '--remote-debugging-port=9222',
        ])

    if browser is None:
        must_close_browser = True

        browser = Browser(timeout=5)

    async def routine():
        await browser.connect()
        target = await browser.call('Target.createTarget', url='about:blank', height=800, width=1200)
        session = await browser.call('Target.attachToTarget', **target, flatten=True)

        frame_tree = await browser.call('Page.getFrameTree', **session)
        frameId = frame_tree['frameTree']['frame']['id']

        await browser.call('Page.setDocumentContent', frameId=frameId, **session, html=html_content())

        code = expression.substitute(spec=vega_spec, scale=scale)

        result = await browser.call('Runtime.evaluate', expression=code, awaitPromise=True, **session)

        screenshot = await browser.call('Page.captureScreenshot', **session)

        with open('screenshot.png', 'wb') as f:

            import base64
            f.write(base64.b64decode(screenshot['data']))

        await browser.call('Target.closeTarget', **target, **session)

        if must_close_browser:
            await browser.close()

        if 'value' in result['result']:
            return json.loads(result['result']['value'])
        else:
            print(result)
            return None

    try:
        response = asyncio.run(routine())
    except Exception:
        logger.exception('Error during procedure', exc_info=True)
        response = None

    if spawn:
        proc.terminate()
    return response
