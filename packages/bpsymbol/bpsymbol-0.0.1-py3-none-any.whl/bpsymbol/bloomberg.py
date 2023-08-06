from bpsymbol.abstract import SymbolAbstract
from bpsymbol.utils import deep_extend

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
        base = deep_extend(self.base, params)
        return base['symbol'] if base['info']['suffix'] == 'US' \
            else '{}.{}'.format(base['symbol'], base['info']['suffix'])

    def naver(self, params={}):
        base = deep_extend(self.base, params)
        return base['symbol']