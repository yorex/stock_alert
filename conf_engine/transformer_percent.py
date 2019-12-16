#coding=utf-8

from transformer import Transformer
import sys; sys.path.append("../");
from helper import toPercent

class PercentTransformer(Transformer):
    def __init__(self):
        pass

    def transform(self, datas):
        assert isinstance(datas, list)
        return toPercent(datas)


#    return [ 1.0*datas[i]/datas[i-1]-1 if i>0 else 0 for i in range(len(datas))]
