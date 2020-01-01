#coding=utf-8

import sys
import os
sys.path.append("../")
from judger import Judger
from helper import toPercent
from utils import getToday

class DownJudger(Judger):
    def __init__(self, steps, is_continue, peak_percent):
        assert isinstance(steps, list) or isinstance(steps, tuple)
        assert isinstance(is_continue, bool)
        if peak_percent:
            assert peak_percent > 0 and peak_percent < 1.0
        self.steps = steps;
        self.is_continue = is_continue;
        self.peak_percent = peak_percent;

    def judge(self, origin_datas, percent_datas):
        assert isinstance(origin_datas, list)
        assert isinstance(percent_datas, list)
        assert len(origin_datas) == len(percent_datas);
        assert len(origin_datas) > 0; 
        # get peak_min
        peak_min = None
        if self.peak_percent:
            peak_min = max(origin_datas)*(1.0-self.peak_percent)
        # steps point
        sp=0
        hit_points=[]
        for i in range(len(origin_datas)) :
            # 超出peak，step匹配重来
            if peak_min and origin_datas[i] < peak_min:
                sp = 0
                hit_points=[]
                continue
            if percent_datas[i] < 0 and abs(percent_datas[i]) >= self.steps[sp]:
                sp += 1
                # 收集负坐标
                hit_points.append(i - len(origin_datas))
            else:
                if self.is_continue:
                    hit_points=[]
                    sp = 0
                    
            if sp == len(self.steps):
                return hit_points
        return False


if __name__ == '__main__':
    origin_datas = [27547.3, 27683.4, 27688.64, 27847.23, 27651.14, 26926.55, 27065.28, 26571.46, 26323.69, 26326.66, 
                    26681.09, 27093.8, 26889.61, 26466.88, 26595.08, 26993.04, 26913.92, 26954.0, 26893.73, 26346.49, 
                    26444.72, 26391.3, 26062.56, 26217.04, 26498.37, 26494.73, 26436.62, 26645.43, 26994.14, 27687.76]
    percent_datas = toPercent(origin_datas)
    print "origin_datas:", origin_datas
    print "percent_datas:", percent_datas

    judger1 = DownJudger([0.01, 0.02, 0.01], False, None)
    assert judger1.judge(origin_datas, percent_datas)

    judger2 = DownJudger([0.01, 0.02, 0.01], True, None)
    assert judger2.judge(origin_datas, percent_datas)
    
    judger3 = DownJudger([0.01, 0.02], True, 0.05)
    assert judger3.judge(origin_datas, percent_datas)
    
    print "all test pass"

    print getToday()
