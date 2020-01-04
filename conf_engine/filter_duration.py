#coding=utf-8

from filter import Filter
import logger

class DurationFilter(Filter):
    def __init__(self, duration, peakWidth):
        self.duration = duration;
        self.peakWidth = peakWidth;

    # return (metas, data_filted), 其中meta是被过滤数据的一些元信息
    def filte(self, datas):
        assert isinstance(datas, list)
        maxLen = max(self.duration, self.peakWidth)
        peak = max([data['dclose'] for data in datas[-maxLen:]])
        datas_filted =  datas[-self.duration:]
        #dates = [ data['date'] for data in datas_filted]
        return ({"peak":peak}, [ data['dclose'] for data in datas_filted])


if __name__ == '__main__':
    duration_filter = DurationFilter(7)
    print duration_filter.filter([10,1,3,3,4,5,6,4,5,45,])
