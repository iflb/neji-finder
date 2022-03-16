from ducts.spi import EventHandler

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        return handler_spec

    async def handle(self, event):
        sync_id = self.helper.SyncID(event.data['sync_id'])
        pubkey = self.helper.pubsub_key_for_sync(sync_id)
        streamkey = self.helper.stream_key_for_sync(sync_id)

        entry = self.helper.StateEntry(event.data)
        entry.entry_type = self.helper.StateEntry.__name__
        await event.session.redis.xadd_and_publish(pubkey, streamkey, **entry)


