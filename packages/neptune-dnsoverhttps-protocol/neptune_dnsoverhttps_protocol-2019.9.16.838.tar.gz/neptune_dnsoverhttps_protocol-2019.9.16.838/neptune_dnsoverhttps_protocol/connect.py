from .protocol import Protocol


class Connection:

    def __init__(self, dispatcher_cls, loop, cert_path, key_path, prefix='dns-request'):
        self.dispatcher_cls = dispatcher_cls
        self.loop = loop
        self.cert_path = cert_path
        self.key_path = key_path
        self.prefix = prefix

    async def start(self):
        print('Starting DNS-over-HTTPS server')
        Protocol(self).start()