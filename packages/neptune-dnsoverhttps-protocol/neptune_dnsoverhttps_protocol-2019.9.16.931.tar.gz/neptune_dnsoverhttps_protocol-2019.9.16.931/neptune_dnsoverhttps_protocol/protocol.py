from aiohttp import web
import ssl
import base64


class Protocol:
    def __init__(self, connector):
        self.connector = connector
        self.app = web.Application(loop=self.connector.loop)
        self.app.add_routes([web.get(f'/{connector.prefix}', self.handle)])
        # self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        # self.ssl_context.load_cert_chain(connector.cert_path, connector.key_path)

    async def handle(self, request):
        dispatcher = self.connector.dispatcher_cls(loop=self.connector.loop)
        if request.method == 'GET':
            query = request.rel_url.query['dns']
            decoded_query = base64.b64decode(query + '=' * (4 - len(query) % 4))
            result = await dispatcher.handle(decoded_query)
            return web.Response(text=base64.b64encode(result).decode('ascii'))
        elif request.method == 'POST':
            pass
        return web.Response(text='1234')

    def start(self):
        web.run_app(self.app)