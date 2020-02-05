#coding=utf-8

from filter import Filter
import logger

# peak过滤仅以dclose数据为准
class PeakFilter(Filter):
    def __init__(self, peakWidth, peakPercent):
        self.peakPercent = peakPercent;
        self.peakWidth = peakWidth;

    # return (metas, data_filted), 其中meta是被过滤数据的一些元信息
    def filte(self, datas):
        assert isinstance(datas, list)
        windowSize = self.peakWidth
        peak = max([data['dclose'] for data in datas[-windowSize:]])
        peak_min = peak*(1.0-self.peakPercent)
        valley = min([data['dclose'] for data in datas[-windowSize:]])
        valley_max = valley*(1.0+self.peakPercent)
        return [ data if data['dclose'] >= peak_min or data['dclose'] <= valley_max else None for data in datas]

    @classmethod
    def parseFilter(self, rule):
        peak_width = None
        peak_percent = None
        if rule.has_key('peak'):
            assert rule['peak'].has_key('height')
            peak_percent = rule['peak']['height']
            assert peak_percent > 0 and peak_percent < 1.0
        if rule.has_key('peak'):
            assert rule['peak'].has_key('width')
            peak_width = min(peak_width, rule['peak']['width'])
        if peak_width and peak_percent:
            return PeakFilter(peak_width, peak_percent)
        else:
            return None
        


if __name__ == '__main__':
    peak_filter = PeakFilter(7, 0.05)
    print peak_filter.filte([{'dclose': v} for v in [10,1,3,3,4,5,6,4,5,45]])
