#coding=utf-8

from filter import Filter
import logger

class DurationFilter(Filter):
    def __init__(self, size):
        self.size = size;

    def filte(self, datas):
        assert isinstance(datas, list)
        datas_filted =  datas[-self.size:]
        #dates = [ data['date'] for data in datas_filted]
        return [ data['dclose'] for data in datas_filted]


if __name__ == '__main__':
    duration_filter = DurationFilter(7)
    print duration_filter.filter([10,1,3,3,4,5,6,4,5,45,])
