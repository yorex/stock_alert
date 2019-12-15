#!/bin/python
#coding=utf-8

def toPercent(datas):
    return [ 1.0*datas[i]/datas[i-1]-1 if i>0 else 0 for i in range(len(datas))]
