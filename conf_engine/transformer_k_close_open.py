#coding=utf-8

from transformer import Transformer
import sys; sys.path.append("../");
from helper import toPercent

class KCloseOpenTransformer(Transformer):
    def __init__(self, windows):
        self.windows = windows

    def transform(self, datas):
        assert isinstance(datas, list)


    @classmethod
    def parseKCloseOpenTransformer(cls, rule):
        seq_type = rule.get("seqType")
        if seq_type and seq_type == 'k:close-open':
            return KCloseOpenTransformer(7)
 

