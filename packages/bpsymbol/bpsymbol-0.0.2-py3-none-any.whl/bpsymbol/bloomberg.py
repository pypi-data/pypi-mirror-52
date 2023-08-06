from bpsymbol.abstract import SymbolAbstract
from bpsymbol.utils import deep_extend

suffix_yahoo_dct = {'US':'', 'IM':'.MI', 'DC':'.CO', 'FH':'.HE', 'BZ':'.SA', 'RM':'.ME', 'CI':'.SN',
                    'AR':'.BA', 'CN':'.TO', 'SS':'.ST', 'LN':'.L', 'MM':'.MX', 'NA':'.AS', 'SM':'.MC',
                    'NO':'.OL', 'CH':'.SS', 'GR':'.DE', 'CH':'.SS'}

class BloombergSymbol(SymbolAbstract):
    def __init__(self, symbol, params={}):
        self.base = deep_extend(self.base, params)
        pure_symbol, suffix, asset_type = symbol.split(' ')[:]

        base = {
            'info': {
            'type': 'bloomberg',
            'symbol': symbol,
            'pure_symbol': pure_symbol,
            'suffix': suffix,
            },

            'symbol': pure_symbol,
            'asset_type': asset_type
        }

        self.base = deep_extend(self.base, base)

    def use(self, feeder='bloomberg', params={}):
        __feeder__ = getattr(self, feeder)
        return __feeder__(params)

    def bloomberg(self, params={}):
        return self._base(params)

    def yahoo(self, params={}):
        fmt = {
            'symbol': symbol,
            'is_us': True if base['info']['suffix'] == 'US' else False,
            'exchange': suffix_yahoo_dct.get(base['info']['suffix'], base['info']['suffix'])
        }
        msg = deep_extend(fmt, params)
        return fmt['symbol'] if fmt['is_us'] == True else '{}.{}'.format(fmt['symbol'], fmt['exchange'])

    def naver(self, params={}):
        base = deep_extend(self.base, params)
        return base['symbol']