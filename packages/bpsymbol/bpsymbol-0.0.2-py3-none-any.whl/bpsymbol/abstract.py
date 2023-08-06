from bpsymbol.utils import deep_extend

class SymbolAbstract:
    base = {
        'info': {
        'type': None,
        'symbol': None,
        'pure_symbol': None,
        'prefix': None,
        'suffix': None,
        },

        'symbol': None,
        'name': None,
        'nation': None,
        'exchange': None,
        'asset_type': None,
    }

    def _base(self, params={}):
        base = deep_extend(self.base, params)
        return base['info']['symbol']