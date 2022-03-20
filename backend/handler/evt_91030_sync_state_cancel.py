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
        sync_id = self.helper.SyncID(event.data.get('sync_id'))
        pubkey = self.helper.pubsub_key_for_state_cancel(sync_id)
        cancel_request_id = event.data.get('cancel_request_id')
        await event.session.redis.execute('PUBLISH', pubkey, cancel_request_id)
        print('CANCEL:::{}:::{}'.format(pubkey, cancel_request_id))
        
