from ducts.spi import EventHandler

import cv2
import numpy as np

from datetime import datetime
from io import BytesIO
from pathlib import Path

import aiofiles

from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

@config_callback
def config(loader):
    loader.add_attr_int('laplacian_score', 50, help='minimum laplacian variance to detect blur')
    loader.add_attr('path_prefix', './htdocs/capture/img/', help='')
    
class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        return handler_spec

    def calc_laplacian(self, data):
        buf = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(buf,cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(img, cv2.CV_64F)
        return lap.var()

    async def handle(self, event):
        score = self.calc_laplacian(event.data['buf'])
        if (score < self.conf.laplacian_score):
            logger.warn('%s < %s', score, self.conf.laplacian_score)
            return {'score:': score, 'error': 'image is out of focus. score is [{}]'.format(score)}
        neji_id = event.data.get('neji', 'unknown')
        user_id = event.data.get('user', 'unknown')
        parent = Path(self.conf.path_prefix, neji_id)
        parent.mkdir(parents = True, exist_ok = True)
        filename = '{}-{}.{}.jpg'.format(user_id, event.session.session_id(), event.session.request_id())
        async with aiofiles.open(str(Path.joinpath(parent, filename)), 'wb') as f:
            await f.write(event.data['buf'])
        return {'score:': score, 'path':neji_id+'/'+filename}
