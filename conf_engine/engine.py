# coding=utf-8
import sys
import os
sys.path.append("../")
import logger
import traceback
from mongoHelper import MongoHelper
from filter_duration import DurationFilter
from transformer_percent import PercentTransformer
from judger_down import DownJudger
from utils import getToday, getYesterday
import json

class RuleChain:
    def __init__(self, name):
        self.name = name;
       
    def parseFilter(self, rule):
        size = 0 
        if rule.has_key('duration'):
            size = max(size, rule['duration'])
        if rule.has_key('peak'):
            assert rule['peak'].has_key('width')
            size = max(size, rule['peak']['width'])
        size = 30 if size == 0 else size
        self.filter = DurationFilter(size)

    def parseTransformer(self, rule):
        self.transformer = PercentTransformer();

    def parseJudger(self, rule):
        downList = []
        is_continue = False
        peak_percent = None
        if rule.has_key('down'):
            downList = rule['down']
            is_continue = False
        if rule.has_key('continueDown'):
            downList = rule['continueDown']
            is_continue = True
        if rule.has_key('peak'):
            assert rule['peak'].has_key('height')
            peak_percent = rule['peak']['height']
        self.judger = DownJudger(downList, is_continue, peak_percent)

    def parseWarnContent(self, rule):
        assert rule.has_key('warn')
        self.warn = rule['warn']


class RuleEngine:
    def __init__(self):
        self.chains = []
        self.subjects = []
        self.mongo= MongoHelper("stock")

    def load(self, conf_pathfile, subjects_pathfile):
        with open(conf_pathfile, "r") as f:
            conf = json.load(f)
        assert conf.has_key('rules')
        rule_conf = conf['rules']
        for rule_name in rule_conf.keys():
            rule = rule_conf[rule_name]
            rule_chain = RuleChain(rule_name);
            rule_chain.parseFilter(rule)
            rule_chain.parseTransformer(rule)
            rule_chain.parseJudger(rule)
            rule_chain.parseWarnContent(rule)
            self.chains.append(rule_chain)

        for subject in  open(subjects_pathfile, "r"): 
            self.subjects.append(subject)

    def run_for_date(self, date=getYesterday()):

        datas_len = max([chain.filter.size for chain in self.chains])
        
        for subject in self.subjects:
            subject = self.get_collection_name(subject)
            datas = self._readData(subject, date, datas_len)
            for chain in self.chains:
                try:
                    datas_filted = chain.filter.filte(datas)
                    #logger.info("datas_filted: %s", datas_filted)
                    datas_transformed = chain.transformer.transform(datas_filted)
                    hit_points = chain.judger.judge(datas_filted, datas_transformed)
                    if hit_points:
                        # date 对应的数据记录
                        cur_data = datas[-1]
                        cur_data.setdefault("warn", {})[chain.name] = chain.warn
                        self.mongo.update(subject, {"_id":cur_data["_id"]}, cur_data)
                        logger.info("subject(%s) chain(%s) -> warn(%s), hit_points(%s) hit_values(%s)", 
                            subject, chain.name, chain.warn, hit_points, [datas_filted[i] for i in hit_points])
                except Exception as e:
                    logger.error("rule(%s) for subject(%s) exception(%s)", chain.name, subject, traceback.format_exc())

    def _readData(self, collection, date, limit):
        datas = self.mongo.find(collection, {"date":{"$lte":date}}, limit)
        #logger.info_print("data: %s", datas)
        return datas

    def get_collection_name(self, subject):
        return "c%s" % subject.replace(".", "").strip()


if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.load("../config/rules.conf", "../config/subjects.conf")
    ruleEngine.run_for_date()
