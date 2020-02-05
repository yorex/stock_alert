#coding=utf-8

from filter import Filter
import logger

class DurationFilter(Filter):
    def __init__(self, duration):
        self.duration = duration;

    def filte(self, datas):
        assert isinstance(datas, list)
        return datas[-self.duration:]

    @classmethod
    def parseFilter(self, rule):
        duration = 30 
        if rule.has_key('duration'):
            duration = min(duration, rule['duration'])
        return DurationFilter(duration)
 

if __name__ == '__main__':
    duration_filter = DurationFilter(7)
    print duration_filter.filter([10,1,3,3,4,5,6,4,5,45,])
