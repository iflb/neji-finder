from ducts.spi import EventHandler

from pathlib import Path
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

from ifconf import configure_module, config_callback

@config_callback
def config(loader):
    loader.add_attr_path('xlsx_path', Path('./neji.xlsx'), help='path to the neji excel file')
    
class Handler(EventHandler):

    def __init__(self):
        super().__init__()
        self.conf = configure_module(config)

    def setup(self, handler_spec, manager):
        handler_spec.set_description('Neji Finder')
        print(self.conf.xlsx_path.absolute());
        try:
            self.neji = manager.load_helper_module('helper_neji').Neji(self.conf.xlsx_path)
        except Exception as e:
            import traceback
            traceback.print_exc()
        print("hoge")
        return handler_spec

    async def handle(self, event):
        call = self.find
        if not event.data:
            return await call()
        if isinstance(event.data, str):
            return await call(event.data)
        elif isinstance(event.data, list):
            return await call(*event.data)
        elif isinstance(event.data, dict):
            return await call(**event.data)
        elif event.data:
            raise ValueError('invalid argument. data=[{}]'.format(event.data))
        else:
            return await call()

    async def find(self, genre = '', query = {}):
        return self.neji.find(genre, **(query if isinstance(query, dict) else {}))
    
