from django.core.management import BaseCommand
from django_vega.browser import Browser
import asyncio


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        async def main():
            c = Browser()

            await c.connect()
            await c.call('Page.enable')

            async def get_svg(**kwargs):
                response = await c.call('Runtime.evaluate',
                                        expression='document.querySelector("#viz svg").outerHTML')
                svg = response['result']['result']['value']
                with open('viz.svg', 'w') as out:
                    out.write(svg)

            async def save_screenshot(**kwargs):
                response = await c.call('Page.captureScreenshot')

                import base64
                with open('screenshot.png', 'wb') as out:
                    b = base64.b64decode(response['result']['data'])
                    out.write(b)

            c.on('Page.loadEventFired', get_svg)
            c.on('Page.loadEventFired', save_screenshot)

            await c.call('Page.navigate', url='http://127.0.0.1:9000/sales/')
            await c.wait(5)

        asyncio.get_event_loop().run_until_complete(main())
