from ducts.spi import EventHandler

import logging
logger = logging.getLogger(__name__)

class Handler(EventHandler):

    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        self.neji = self.helper.Neji()        
        self.event_handler = {}
        self.event_handler[self.helper.ImageEntry.__name__] = self.handle_file_add_entry
        self.event_handler[self.helper.StateEntry.__name__] = self.handle_state_update_entry
        self.event_handler[self.helper.WarningEntry.__name__] = self.handle_warning_entry
        return handler_spec

    async def handle(self, event):
        if not 'sync_id' in event.data:
            sync_id = self.helper.SyncID()
            last_id = '-'
            entry = self.helper.SyncStart()
            entry.sync_id = sync_id.base64
            entry.entry_type = self.helper.SyncStart.__name__
            yield entry
        else:
            sync_id = self.helper.SyncID(event.data.get('sync_id'))
            last_id = event.data.get('last_entry_id') if 'last_entry_id' in event.data else '-'
        subkey = self.helper.pubsub_key_for_sync(sync_id)
        streamkey = self.helper.stream_key_for_sync(sync_id)
        async for stream_id, kv in self.psub_and_xrange_str_from(event.session.redis, subkey, streamkey, last_id):
            ret = await self.event_handler.get(kv['entry_type'], self.handle_else)(event, sync_id, stream_id, kv)
            if ret:
                yield ret
            
    async def handle_file_add_entry(self, event, sync_id, stream_id, kv):
        entry = self.helper.ImageEntry(kv)
        entry.sync_id = sync_id.base64
        entry.content = await self.helper.read_image_for(sync_id, entry.filename)
        return entry
    
    async def handle_state_update_entry(self, event, sync_id, stream_id, kv):
        entry = self.helper.StateEntry(kv)
        entry.sync_id = sync_id.base64
        entry.update(self.neji.find(entry.genre, entry.query))
        return entry

    async def handle_warning_entry(self, event, sync_id, stream_id, kv):
        entry = self.helper.WarningEntry(kv)
        entry.sync_id = sync_id.base64
        return entry

    async def handle_else(self, event, stream_id, kv):
        pass
        
    
    async def psub_and_xrange_str_from(self, redis, subkey, streamkey, last_id = '-'):
        pubsub_channel_iter = None
        while True:
            ret = await redis.execute_str('XRANGE', streamkey, last_id, '+', 'COUNT', 10)
            if ret is not None and len(ret) > 0:
                for result in ret:
                    if result[0] <= last_id:
                        continue
                    yield [result[0], {v[0] : v[1] for v in zip(*[iter(result[1])]*2)}]
                    last_id = result[0]
            else:
                if pubsub_channel_iter is None:
                    ch = (await redis.psubscribe(subkey))
                    pubsub_channel_iter = (ch.iter())
                    pubsub_channel_iter = type(pubsub_channel_iter).__aiter__(pubsub_channel_iter)
                try:
                    ch, msg = await type(pubsub_channel_iter).__anext__(pubsub_channel_iter)
                except StopAsyncIteration:
                    break
