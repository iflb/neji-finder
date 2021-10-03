import pandas as pd

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
    
    def __init__(self, xlsx_path):
        ##df = pd.read_excel(xlsx_path, header=2)
        df = pd.read_pickle('neji.pkl')
        
        df.rename(columns={'長さ・厚み':'長さか厚み', '外径・幅':'外径か幅'}, inplace=True)
        self.neji = {g : df[df['おねじ・めねじ・座金'] == g] for g in Neji.GENRE}

    def find(self, genre, **selected):
        if not genre:
            return {'genres':Neji.GENRE}
        try:
            df = self.neji[genre].query('&'.join([' {} == "{}" '.format(k,v) for k,v in selected.items()])) if selected else self.neji[genre]
        except Exception as e:
            return {'genres':Neji.GENRE, 'error':str(e)}
        if len(df) == 0:
            return {'genres':Neji.GENRE}
        shape = {shape: df[shape].unique().tolist() for shape in Neji.SHAPE[genre]}
        if max([len(v) for v in shape.values()]) > 1:
            return {'genre':genre, 'query':selected, 'shape':shape}
        spec = {spec: df[spec].unique().tolist() for spec in Neji.SPEC[genre]}
        if len(df) <= 100:
            return {'genre':genre, 'query':selected, 'shape':shape, 'spec':spec, 'items':df.to_dict('records')}
        else:
            return {'genre':genre, 'query':selected, 'shape':shape, 'spec':spec }
