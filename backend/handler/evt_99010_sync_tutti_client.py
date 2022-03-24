from ducts.spi import EventHandler

import asyncio
import aioredis

from neji_finder_tutti_client.main import NejiFinderTuttiClient

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

@config_callback
def config(loader):
    #loader.add_attr('automation_parameter_set_id', '6df2299f119e3f9f70d471b86364e356ddebc5e9')
    #loader.add_attr('automation_parameter_set_id', '06e07e2094e95e77cb954d4e818dfd710c1ceebb')
    loader.add_attr('automation_parameter_set_id', '5aa5389d3c567080e0d70da29b3f6c9904fbd77a')
    loader.add_attr('works_host', 'https://dev.neji-finder.tutti.works', help='host url for tutti.works')
    loader.add_attr('market_host', 'https://dev.neji-finder.tutti.market', help='host url for tutti.market')
    loader.add_attr_dict('works_params', {'user_name': 'admin', 'password': 'admin'}, help='Parameters for tutti.market')
    loader.add_attr_dict('market_params', { 'user_id': 'requester1', 'password': 'requester1' }, help='Parameters for or tutti.market')

class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        self.helper = manager.load_helper_module('helper_neji')
        return handler_spec

    async def run(self, manager):
        
        last_id = await manager.redis.execute_str('GET', self.helper.str_key_for_sync_tutti())
        print(last_id)
        last_id = last_id if last_id else '0-0'
        subkey = self.helper.pubsub_key_for_sync()
        streamkey = self.helper.stream_key_for_sync()

        tutti = NejiFinderTuttiClient()
        await tutti.open(works_host = self.conf.works_host, market_host = self.conf.market_host)
        await tutti.sign_in(works_params = self.conf.works_params, market_params = self.conf.market_params)
        
        while True:
            try:
                #logger.info('**************** 0')
                #redis = await aioredis.create_redis(manager.redis.conf.redis_uri_main)
                #logger.info('**************** 1.REDIS=%s', redis)
                #ret = await redis.execute('XREAD', 'COUNT', 1, 'BLOCK', 10000, 'STREAMS', streamkey, last_id)
                #logger.info('**************** 2.XREAD=%s', ret)
                logger.info('**************** 1.REDIS=%s', manager.redis)
                async for last_id, kv in self.psub_and_xrange_str(manager.redis, subkey, streamkey, last_id):
                    logger.info('**************** 2.ID=%s, KV=%s', last_id, kv)
                    if 'sync_id' not in kv:
                        logger.warning('sync_id is not included. kv=%s', kv)
                    else:
                        sync_id = kv['sync_id']
                        logger.info('**************** 3.SYNC_ID=%s', sync_id)
                        ngid, jid = await tutti.publish_tasks_to_market(
                            self.conf.automation_parameter_set_id,
                            sync_id
                        )
                        logger.info('**************** 4.task is created. ngid=%s, jid=%s', ngid, jid)
                    await manager.redis.execute_str('SET', self.helper.str_key_for_sync_tutti(), last_id)
            except:
                logger.exception('********************Error occurred in sync_tutti_client#run**********************')
                await asyncio.sleep(1)
                break

    async def psub_and_xrange_str(self, redis, subkey, streamkey, last_id):
        ch = (await redis.psubscribe(subkey))
        pubsub_channel_iter = (ch.iter())
        pubsub_channel_iter = type(pubsub_channel_iter).__aiter__(pubsub_channel_iter)
        while True:
            ret = await redis.execute_str('XRANGE', streamkey, last_id, '+')
            logger.debug('********** XRANGE|RET=%s', ret)
            for stream_id, data in ret if ret else []:
                if stream_id > last_id:
                    last_id = stream_id
                    yield last_id, {v[0] : v[1] for v in zip(*[iter(data)]*2)}
            try:
                ch, msg = await type(pubsub_channel_iter).__anext__(pubsub_channel_iter)
                logger.info('********** NOTIFIED|CH=%s|MSG%s}', ch, msg)
            except StopAsyncIteration:
                break
                
    async def handle(self, event):
        sync_id = self.helper.SyncID(event.data['sync_id'])
        pubkey = self.helper.pubsub_key_for_state(sync_id)
        streamkey = self.helper.stream_key_for_state(sync_id)
        entry = self.helper.StateEntry({k:(v if type(v) is str else json.dumps(v)) for k,v in event.data.items() if v})
        await event.session.redis.xadd_and_publish(pubkey, streamkey, **entry)


