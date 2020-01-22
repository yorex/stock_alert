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
from judger_up import UpJudger
from utils import getFormalCode, getToday, getYesterday, parseConfigSubject, parseCustomWarns
import json

DRY_RUN=False
DEBUG=False

class RuleChain:
    def __init__(self, name):
        self.name = name;
        self.subjects = {}
       
    def parseFilter(self, rule):
        duration = 30 
        peakWidth = 30
        if rule.has_key('duration'):
            duration = min(duration, rule['duration'])
        if rule.has_key('peak'):
            assert rule['peak'].has_key('width')
            peakWidth = min(peakWidth, rule['peak']['width'])
        self.filter = DurationFilter(duration, peakWidth)

    def parseTransformer(self, rule):
        self.transformer = PercentTransformer();

    def parseJudger(self, rule):
        self.judger = DownJudger.parseDownJudger(rule)
        if not self.judger:
            self.judger = UpJudger.parseUpJudger(rule)
        assert self.judger

    def parseWarnContent(self, rule):
        assert rule.has_key('warn')
        self.warn = rule['warn']
    
    def parseSubjects(self, rule):
        if rule.has_key("subjects"):
            assert isinstance(rule['subjects'], list)
            for subject in rule['subjects']:
                self.subjects[getFormalCode(subject)] = 1


class RuleEngine:
    def __init__(self):
        self.chains = []
        self.subjects = []
        self.mongo= MongoHelper("stock")
        self.dryRun=DRY_RUN
        self.custom_warns = {}

    def load(self, conf_pathfile, subjects_pathfile, customwarns_pathfile):
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
            rule_chain.parseSubjects(rule)
            self.chains.append(rule_chain)

        for subject in parseConfigSubject(subjects_pathfile):
            self.subjects.append(subject["fcode"])

        self.custom_warns=parseCustomWarns(customwarns_pathfile);

    def run_for_date(self, date=getYesterday()):

        datas_len = max([max(chain.filter.peakWidth, chain.filter.duration) for chain in self.chains])
        all_warns_ret = []
        
        for subject in self.subjects:
            datas = self._readData(subject, date, datas_len)
            for chain in self.chains:
                try:
                    # filte chain subject 
                    if len(chain.subjects) > 0 and not chain.subjects.has_key(subject):
                        continue

                    metas, datas_filted = chain.filter.filte(datas)
                    if DEBUG:
                        logger.info("chain(%s) datas_filted: %s", chain.name, datas_filted)
                    datas_transformed = chain.transformer.transform(datas_filted)
                    hit_points = chain.judger.judge(datas_filted, datas_transformed, metas)
                    if hit_points:
                        # date 对应的数据记录
                        cur_data = datas[-1]
                        warn = chain.warn
                        custom_warn = self._get_custom_warn(subject, chain.name, date)
                        if custom_warn:
                            warn += "@" + custom_warn
                        cur_data.setdefault("warn", {})[chain.name] = warn
                        self._writeData(subject, {"_id":cur_data["_id"]}, cur_data)
                        record = "%s date(%s) subject(%s) chain(%s) -> warn(%s), hit_points(%s) hit_values(%s)" % ("DRY-RUN" if self.dryRun else "", cur_data["date"], subject, chain.name, warn, hit_points, [datas_filted[i] for i in hit_points])
                        logger.info(record)
                        all_warns_ret.append(record)
                except Exception as e:
                    logger.error("rule(%s) for subject(%s) exception(%s)", chain.name, subject, traceback.format_exc())
        return all_warns_ret

    def _get_custom_warn(self, subject, chain_name, date):
        if len(self.custom_warns) > 0:
            warn_id = "%s_%s" % (subject, chain_name)
            warn = self.custom_warns.get(warn_id)
            monthday=date[4:]
            if warn:
                if warn.get("begin") and monthday < warn.get("begin"):
                    return ""
                if warn.get("end") and monthday > warn.get("end"):
                    return ""
                return warn.get("warn")
        return ""
    
    def _writeData(self, collection, query, data):
        if not self.dryRun:
            self.mongo.update(collection, query, data)

    def _readData(self, collection, date, limit):
        datas = self.mongo.find(collection, {"date":{"$lte":date}}, limit)
        #logger.info_print("data: %s", datas)
        return datas


if __name__ == "__main__":
    ruleEngine = RuleEngine()
    ruleEngine.load("../config/rules.conf", "../config/subjects.conf", "../config/custom_warns")
    ruleEngine.run_for_date()
