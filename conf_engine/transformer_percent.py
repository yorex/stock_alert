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


