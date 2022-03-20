import pandas as pd

import cv2
import numpy as np

import json

import hashlib
import base64
import struct
import random
import abc
from datetime import datetime
from functools import reduce

import asyncio
import aiofiles

from iflb import nameddict
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)
        
@config_callback
def config(loader):
    loader.add_attr_path('path_neji_pkl', './neji.pkl', help='')
    loader.add_attr_path('path_prefix', './htdocs/img/', help='')

conf = configure_module(config)

class Neji:
    
    GENRE = ['おねじ', 'めねじ', '座金']
    SHAPE = {
        'おねじ': ['頭部', 'おねじ先端', '頭部穴形状'],
        'めねじ': ['ナット形状'],
        '座金': ['座金形状']
    }
    SPEC = {
        'おねじ': ['中分類', '呼び径',             '長さか厚み', '材質', '表面処理', '構成数クラス'],
        'めねじ': ['中分類', '呼び径',                           '材質', '表面処理', '構成数クラス'],
        '座金':   ['中分類', '呼び径', '外径か幅', '長さか厚み', '材質', '表面処理', '構成数クラス']
    }
    
    def __init__(self):
        ##df = pd.read_excel(xlsx_path, header=2)
        df = pd.read_pickle(str(conf.path_neji_pkl))
        
        df.rename(columns={'長さ・厚み':'長さか厚み', '外径・幅':'外径か幅'}, inplace=True)
        self.neji = {g : df[df['おねじ・めねじ・座金'] == g] for g in Neji.GENRE}

    def find(self, genre, query):
        if not genre:
            return {'genres':Neji.GENRE}
        try:
            df = self.neji[genre].query('&'.join([' {} == "{}" '.format(k,v) for k,v in query.items()])) if query else self.neji[genre]
        except Exception as e:
            return {'genres':Neji.GENRE, 'error':str(e)}
        if len(df) == 0:
            return {'genres':Neji.GENRE}
        shape = {shape: df[shape].unique().tolist() for shape in Neji.SHAPE[genre]}
        if max([len(v) for v in shape.values()]) > 1:
            return {'genre':genre, 'query':query, 'shape':shape}
        spec = {spec: df[spec].unique().tolist() for spec in Neji.SPEC[genre]}
        if len(df) <= 100:
            return {'genre':genre, 'query':query, 'shape':shape, 'spec':spec, 'items':df.to_dict('records')}
        else:
            return {'genre':genre, 'query':query, 'shape':shape, 'spec':spec }


class DateHashID(metaclass=abc.ABCMeta):
    
    @staticmethod
    def define(cls_name, datetime_format, hashfunc = hashlib.sha1):
        hex_str = hashfunc(b'').hexdigest()
        hash_length = len(hex_str)
        base64_length = len(base64.b64encode(hex_str.encode('UTF-8') + datetime.now().strftime(datetime_format).encode('UTF-8')))
        return type(cls_name,
                    (DateHashID,),
                    {"DATETIME_FORMAT": datetime_format,
                     "hash": lambda self, buf: hashfunc(buf),
                     "HASH_LENGTH": hash_length,
                     "BASE64_LENGTH": base64_length})
    
    def __init__(self, b64_str = None):
        if b64_str:
            if type(b64_str) is not str:
                raise ValueError('b64_str is not str but {}'.format(type(b64_str)))
            if len(b64_str) != self.BASE64_LENGTH:
                raise ValueError('len(b64_str) must be {} but was {}'.format(self.BASE64_LENGTH, len(b64_str)))
            self._b64_str = b64_str
            self._b64 = self._b64_str.encode('UTF-8')
            self._dhid = [f(v).decode('UTF-8') for f,v in zip([lambda v:v[:self.HASH_LENGTH], lambda v:v[self.HASH_LENGTH:]], [base64.b64decode(self._b64)]*2)]
        else:
            self._dhid = [f(dt) for f,dt in
                          zip([lambda dt: self.hash(struct.pack('d', dt.timestamp()+random.random())).hexdigest(), lambda dt: dt.strftime(self.DATETIME_FORMAT)],
                              [datetime.now()]*2)]
            self._b64 = base64.b64encode(reduce(lambda a, b: a + b.encode('UTF-8'), self._dhid, b''))
            self._b64_str = self._b64.decode('UTF-8')
            
    @property
    @abc.abstractmethod
    def hash(self, buf):
        pass
    
    @property
    def hash_id(self):
        return self._dhid[0]
    
    @property
    def date_str(self):
        return self._dhid[1]
    
    @property
    def base64(self):
        return self._b64_str
    








SyncID = DateHashID.define('SyncID', '%Y%m%d/%H')

ImageEntry = nameddict(
    'ImageEntry',
    (
        'sync_id',
        'filename',
        'score',
        'content_length',
        'content',
        'error',
    ))

StateEntry = nameddict(
    'StateEntry',
    (
        'sync_id',
        'updated',
        'genre',
        'query',
        'response',
    ))

def stream_key_for_sync():
    return f'SYNC/IDS'


def pubsub_key_for_state(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/STATE/PUBSUB'

def pubsub_key_for_state_cancel(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/STATE/CANCEL'

def psub_key_for_state(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/STATE/*'

def stream_key_for_state(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/STATE/STREAMS'


def pubsub_key_for_img(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/IMG/PUBSUB'

def stream_key_for_img(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/IMG/STREAMS'

def incr_key_for_img(sync_id):
    return f'SYNC/SID={sync_id.hash_id}/IMG/INCR'


def calc_laplacian(data):
    buf = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(buf,cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(img, cv2.CV_64F)
    return float(lap.var())

async def read_image_for(sync_id, filename):
    filepath = conf.path_prefix.joinpath(sync_id.date_str, sync_id.hash_id, filename)
    async with aiofiles.open(str(filepath), 'rb') as f:
        return await f.read()

async def write_image_for(sync_id, filename, data):
    filedir = conf.path_prefix.joinpath(sync_id.date_str, sync_id.hash_id)
    filedir.mkdir(parents=True, exist_ok=True)
    filepath = filedir.joinpath(filename)
    async with aiofiles.open(str(filepath), 'wb') as f:
        await f.write(data)

        
