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
        subkey = self.helper.pubsub_key_for_img(sync_id)
        streamkey = self.helper.stream_key_for_img(sync_id)
        async for stream_id, kv in self.psub_and_xrange_str_from(event.session.redis, subkey, streamkey, '-'):
            entry = self.helper.ImageEntry(kv)
            entry.sync_id = sync_id.base64
            print('#####################{}'.format(entry))
            
            if entry.filename:
                entry.content = await self.helper.read_image_for(sync_id, entry.filename)
            yield entry
            
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
