#coding=utf-8

import sys
import os
sys.path.append("../")
from judger import Judger
from helper import toPercent
from utils import getToday

class UpJudger(Judger):
    @classmethod
    def parseUpJudger(cls, rule):
        upList = []
        is_continue = False
        if rule.has_key('up'):
            upList = rule['up']
            is_continue = False
        if rule.has_key('continueUp'):
            upList = rule['continueUp']
            is_continue = True
        if upList:
            return UpJudger(upList, is_continue)
        else:
            return None

    def __init__(self, steps, is_continue):
        assert isinstance(steps, list) or isinstance(steps, tuple)
        assert isinstance(is_continue, bool)
        self.steps = steps;
        self.is_continue = is_continue;

    def judge(self, percent_datas):
        assert isinstance(percent_datas, list)
        assert len(percent_datas) > 0; 
        # steps point
        sp=0
        hit_points=[]
        for i in range(len(percent_datas)) :
            # 超出valley，step匹配重来
            if percent_datas[i] == None: 
                sp = 0
                hit_points=[]
                continue
            if percent_datas[i] > 0 and abs(percent_datas[i]) >= self.steps[sp]:
                sp += 1
                # 收集负坐标
                hit_points.append(i - len(percent_datas))
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
    #valley_datas = [ data if data < metas['valley']*(1+valley_height) else 1 for data in origin_datas]
    #valley_percent_datas = toPercent(valley_datas)
    print "origin_datas:", origin_datas
    print "percent_datas:", [int(percent*10000)/10000.0 for percent in percent_datas]
    #print "valley datas: ", valley_datas
    #print "valley percent datas: ", [int(percent*10000)/10000.0 for percent in valley_percent_datas]


    judger1 = UpJudger([0.01, 0.01, 0.02], False)
    assert judger1.judge(origin_datas, percent_datas)

    judger2 = UpJudger([0.007, 0.01, 0.01], True)
    assert judger2.judge(origin_datas, percent_datas)
    
    judger3 = UpJudger([0.005, 0.01], True)
    assert judger3.judge(origin_datas, percent_datas)
    
    print "all test pass"

    print getToday()
