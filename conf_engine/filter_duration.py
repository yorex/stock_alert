#coding=utf-8

from filter import Filter

class DurationFilter(Filter):
    def __init__(self, name, num):
        self.num = num;
        self.name = name;

    def name(self):
        return self.name;

    def filter(self, datas):
        assert isinstance(datas, list)
        return datas[0:self.num]


if __name__ == '__main__':
    duration_filter = DurationFilter("durationFilter", 7)
    print duration_filter.name, duration_filter.filter([10,1,3,3,4,5,6,4,5,45,])
