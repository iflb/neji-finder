from ducts.spi import EventHandler

import json

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        return handler_spec

    async def handle(self, event):
        sync_id = self.helper.SyncID()
        streamkey = self.helper.stream_key_for_sync()
        await event.session.redis.xadd(streamkey, sync_id = sync_id.base64)
        return {'sync_id': sync_id.base64}

