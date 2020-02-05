#coding=utf-8

from transformer import Transformer
import sys; sys.path.append("../");
from helper import toPercent
import logger

class KCloseOpenTransformer(Transformer):
    def __init__(self, windows):
        self.windows = windows

    def transform(self, datas):
        assert isinstance(datas, list)
        #和前面windows天均值比较 
        datas = [data['dclose']-data['dopen'] for data in datas]
        #logger.info("transform:datas: %s", datas)
        percents = []
        for i in range(len(datas)):
            if i >= self.windows:
                sum = 0
                cnt = 0
                for j in range(self.windows):        
                    if datas[i] * datas[i-j-1] > 0:
                        #logger.info("hit point: %s %s", datas[i], datas[i-j-1])
                        sum += datas[i-j-1]
                        cnt += 1
                avg = sum/cnt
                percents.append(datas[i]/avg)
            else:
                percents.append(None)
        return percents


    @classmethod
    def parseTransformer(cls, rule):
        seq_type = rule.get("seqType")
        if seq_type and seq_type == 'k:close-open':
            return KCloseOpenTransformer(7)
        else:
            return None
 

