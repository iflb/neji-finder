from ducts.spi import EventHandler

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

def config(loader):
    loader.add_attr_int('laplacian_score', 50, help='minimum laplacian variance to detect blur')
    
class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        return handler_spec

    async def handle(self, event):
        sync_id = self.helper.SyncID(event.data['sync_id'])

        pubkey = self.helper.pubsub_key_for_sync(sync_id)
        streamkey = self.helper.stream_key_for_sync(sync_id)
        incrkey = self.helper.incr_key_for_sync(sync_id)
        
        score = self.helper.calc_laplacian(event.data['buf'])
        if (score < self.conf.laplacian_score):
            logger.warn('%s < %s', score, self.conf.laplacian_score)
            entry = self.helper.WarningEntry()
            entry.entry_type = self.helper.WarningEntry.__name__
            entry.sync_id = sync_id.base64
            entry.message = 'image is out of focus. score is [{}]'.format(score)
            await event.session.redis.xadd_and_publish(pubkey, streamkey, **entry)
        else:
            entry = self.helper.ImageEntry()
            entry.entry_type = self.helper.ImageEntry.__name__
            entry.sync_id = sync_id.base64
            entry.filename = "{:06d}.jpg".format(int(await event.session.redis.execute_str('INCR', incrkey)))
            entry.score = score
            entry.content_length = len(event.data['buf'])
            print("*****************************{}".format(entry))
            await self.helper.write_image_for(sync_id, entry.filename, event.data['buf'])
            await event.session.redis.xadd_and_publish(pubkey, streamkey, **entry)

