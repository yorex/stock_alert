# coding=utf-8
import sys
import os
sys.path.append("../")
import logger
import traceback
from mongoHelper import MongoHelper
from filter_duration import DurationFilter
from filter_peak import PeakFilter
from transformer_percent import PercentTransformer
from transformer_k_close_open import KCloseOpenTransformer
from judger_down import DownJudger
from judger_up import UpJudger
from utils import getFormalCode, getToday, getYesterday, parseConfigSubject, parseCustomWarns, parseRuleConfig
import json

DRY_RUN=False
#DRY_RUN=True
DEBUG=False
#DEBUG=True

class RuleChain:
    def __init__(self, name):
        self.name = name;
        self.subjects = {}
       
    def parsePreFilter(self, rule):
        self.pre_filter = PeakFilter.parseFilter(rule)

    def parsePostFilter(self, rule):
        self.post_filter = DurationFilter.parseFilter(rule)
        assert self.post_filter

    def parseTransformer(self, rule):
        self.transformer = KCloseOpenTransformer.parseTransformer(rule) or PercentTransformer.parseTransformer(rule)
        assert self.transformer

    def parseJudger(self, rule):
        self.judger = DownJudger.parseDownJudger(rule) or UpJudger.parseUpJudger(rule)
        #if not self.judger:
        #    self.judger = UpJudger.parseUpJudger(rule)
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
        conf = parseRuleConfig(conf_pathfile)
        assert conf and conf.has_key('rules')

        rule_conf = conf['rules']
        for rule_name in rule_conf.keys():
            rule = rule_conf[rule_name]
            rule_chain = RuleChain(rule_name);

            rule_chain.parsePreFilter(rule)
            rule_chain.parseTransformer(rule)
            rule_chain.parsePostFilter(rule)
            rule_chain.parseJudger(rule)
            rule_chain.parseWarnContent(rule)
            rule_chain.parseSubjects(rule)
            self.chains.append(rule_chain)

        for subject in parseConfigSubject(subjects_pathfile):
            self.subjects.append(subject["fcode"])

        self.custom_warns=parseCustomWarns(customwarns_pathfile);

    def run_for_date(self, date=getYesterday()):

        datas_len = max([max(chain.pre_filter.peakWidth if chain.pre_filter else 0, chain.post_filter.duration) for chain in self.chains])
        all_warns_ret = []
        
        for subject in self.subjects:
            datas = self._readData(subject, date, datas_len)
            for chain in self.chains:
                try:
                    # first: filte chain subject 
                    if len(chain.subjects) > 0 and not chain.subjects.has_key(subject):
                        continue
                    # second: pre-filte
                    if chain.pre_filter:
                        datas_pre_filted = chain.pre_filter.filte(datas)
                    else:
                        datas_pre_filted = datas
                    if DEBUG:
                        logger.info("chain(%s) datas_pre_filted: %s", chain.name, datas_pre_filted)
                    datas_transformed = chain.transformer.transform(datas_pre_filted)
                    if DEBUG:
                        logger.info("chain(%s) datas_transformed: %s", chain.name, datas_transformed)
                    datas_post_filted = chain.post_filter.filte(datas_transformed)
                    if DEBUG:
                        logger.info("chain(%s) datas_post_filted: %s", chain.name, datas_post_filted)
                    hit_points = chain.judger.judge(datas_post_filted)
                    if hit_points:
                        # date 对应的数据记录
                        cur_data = datas[-1]
                        warn = chain.warn
                        custom_warn = self._get_custom_warn(subject, chain.name, date)
                        if custom_warn:
                            warn += "@" + custom_warn
                        cur_data.setdefault("warn", {})[chain.name] = warn
                        self._writeData(subject, {"_id":cur_data["_id"]}, cur_data)
                        record = "%s date(%s) subject(%s) chain(%s) -> warn(%s), hit_points(%s) hit_values(%s)" % ("DRY-RUN" if self.dryRun else "", cur_data["date"], subject, chain.name, warn, hit_points, [datas_post_filted[i] for i in hit_points])
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
