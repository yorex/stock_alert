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
        # get peak_min
        peak_min = None
        if self.peak_percent:
            peak_min = max(origin_datas)*(1.0-self.peak_percent)
        # steps point
        sp=0
        for i in range(len(origin_datas)) :
            # 超出peak，step匹配重来
            if peak_min and origin_datas[i] < peak_min:
                sp = 0
                continue
            if percent_datas[i] <= self.steps[sp]:
                sp += 1
            else:
                if self.is_continue:
                    sp = 0
                    
            if sp == len(self.steps):
                return True
        return False


if __name__ == '__main__':
    origin_datas = [13,17,15,16,13,10,11,9,8]
    percent_datas = toPercent(origin_datas)
    print "origin_datas:", origin_datas
    print "percent_datas:", percent_datas

    judger1 = DownJudger("warning", [0.01, 0.02, 0.01], False, None)
    assert judger1.judge(origin_datas, percent_datas)

    judger2 = DownJudger("warning", [0.01, 0.02, 0.01], True, None)
    assert not judger2.judge(origin_datas, percent_datas)
    
    judger3 = DownJudger("warning", [0.01, 0.02], True, 0.05)
    assert not judger3.judge(origin_datas, percent_datas)
    
    print "all test pass"

    print getToday()
