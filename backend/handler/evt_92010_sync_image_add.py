from ducts.spi import EventHandler

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

def config(loader):
    loader.add_attr_int('laplacian_score', 30, help='minimum laplacian variance to detect blur')
    
class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        return handler_spec

    async def handle(self, event):
        sync_id = self.helper.SyncID(event.data['sync_id'])

        pubkey = self.helper.pubsub_key_for_img(sync_id)
        streamkey = self.helper.stream_key_for_img(sync_id)
        incrkey = self.helper.incr_key_for_img(sync_id)
        
        buf = event.data['buf']
        score = self.helper.calc_laplacian(buf)

        entry = self.helper.ImageEntry()
        entry.sync_id = sync_id.base64
        entry.score = score
        entry.content_length = len(buf)
        if (score < self.conf.laplacian_score):
            logger.warn('%s < %s', score, self.conf.laplacian_score)
            entry.error = 'image is out of focus. score is [{}]'.format(score)
        else:
            entry.filename = "{:06d}.jpg".format(int(await event.session.redis.execute_str('INCR', incrkey)))
            await self.helper.write_image_for(sync_id, entry.filename, buf)

        logger.debug('****************** IMG_ADD=%s', entry)
        await event.session.redis.xadd_and_publish(pubkey, streamkey, **entry)


