from ducts.spi import EventHandler

import json

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        self.neji = self.helper.Neji()        
        return handler_spec
    
    async def handle(self, event):
        sync_id = self.helper.SyncID(event.data.get('sync_id'))
        subkey = self.helper.pubsub_key_for_state(sync_id)
        streamkey = self.helper.stream_key_for_state(sync_id)
        async for updated, stream_id, kv in self.psub_and_xlast_str(event.session.redis, subkey, streamkey):
            entry = self.helper.StateEntry(kv)
            entry.sync_id = sync_id.base64
            entry.updated = updated
            entry.update(self.neji.find(entry.genre, json.loads(entry.query) if entry.query else {}))
            yield entry
    
    async def psub_and_xlast_str(self, redis, subkey, streamkey):
        last_id, kv = await redis.xlast_str_with_id(streamkey)
        yield 0, last_id, kv
        pubsub_channel_iter = None
        while True:
            result = await redis.xlast_str_with_id(streamkey)
            print('*********************{}'.format(result))
            if result[0] > last_id:
                last_id = result[0]
                yield 1, result[0], result[1]
            else:
                if pubsub_channel_iter is None:
                    ch = (await redis.psubscribe(subkey))
                    pubsub_channel_iter = (ch.iter())
                    pubsub_channel_iter = type(pubsub_channel_iter).__aiter__(pubsub_channel_iter)
                try:
                    ch, msg = await type(pubsub_channel_iter).__anext__(pubsub_channel_iter)
                except StopAsyncIteration:
                    break
                
