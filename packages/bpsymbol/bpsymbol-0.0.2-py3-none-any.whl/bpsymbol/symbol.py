from bpsymbol.bloomberg import BloombergSymbol
"""
[*] Bloomberg
    005380 KS Equity

[*] Yahoo
    005380.KS

[*] Cybos
    A005380

[*] Naver
    005380


"""



class Symbol:
    __client__ = None
    __base__ = None
    def __init__(self, symbol, base='bloomberg', params={}):
        self.__base__ = base
        self.__client__ = Symbol.set_base(self.__base__)(symbol=symbol, params=params)

    def use(self, feeder='bloomberg', params={}):
        __feeder__ = getattr(self.__client__, feeder)
        return __feeder__(params)

    @staticmethod
    def set_base(base):
        if base == 'bloomberg':
            return BloombergSymbol

    @property
    def base(self):
        return self.__client__.base