# coding=utf-8

from flask import Flask
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

import io
import random
import json
import rule_engine
import helper
import logger
from flask import jsonify, request
from flask import render_template
from mongoHelper import MongoHelper
from report import AlertSummary

mahelper = helper.MaHelper()


##
# data format:
#   {
#       "dates":[],
#       "balances":[],
#       "hongsengIndex":[],
#       "ruleEmergCount":[1,3,2],
#       "ruleEmerg":[[],[],[]],
#       "ruleWarnCount":[1,3,2],
#       "ruleWarn":[]
#    }
#
@app.route('/getBalanceHsiLocal')
def get_hangseng_index_local():
    logger.debug("getBalanceHsi")
    with open('static/data/balance_hsi.dat', 'r') as fp:
        dates=[]
        balances=[]
        hongsengIndex=[]
        for line in fp:
            if not line or len(line)==0: 
                continue
            items = line.strip().split()
            if len(items) != 3:
                logger.error("getBalanceHsi, invalid data line(%s)", line)
                continue
            dates.append(items[0])
            hongsengIndex.append(float(items[1]))
            balances.append(int(items[2]))
        engine = rule_engine.RuleEngine(app)
#        engine.add_rule(rule_engine.SequenceMonotonicityRule(app, hongsengIndex))
        #ma5sequences = mahelper.getMa(5, hongsengIndex)
        #engine.add_rule(rule_engine.SequenceMonotonicityRule(app, ma5sequences))
        engine.add_rule(rule_engine.RapidDownRule(app, hongsengIndex, 1.02))
        alerts = engine.inspect()
        logger.debug("alerts: %s", alerts)

        return jsonify({
            "dates":dates,
            "balances":balances,
            "hongsengIndex":hongsengIndex,
            "ruleEmergCount":[len(x) for x in alerts[rule_engine.EMERG]],
            "ruleEmerg":alerts[rule_engine.EMERG],
            "ruleWarnCount":[len(x) for x in alerts[rule_engine.WARN]],
            "ruleWarn":alerts[rule_engine.WARN]
        })



@app.route('/getBalanceHsiYahoo')
def get_hangseng_index_yahoo():
    logger.debug("getBalanceHsiYahoo")
    hangsengHelper = MongoHelper("127.0.0.1", "stock" )
    dates=[]
    volumes=[]
    hongsengIndex=[]
    emergs=[]
    warns=[]
    hangseng_datas = hangsengHelper.find("hangseng_index", {})
    for rec in hangseng_datas:
        dates.append(rec["date"])
        hongsengIndex.append(rec["dclose"])
        volumes.append(rec["volume"])

    emergs=MongoHelper.get_alert_emergs(hangseng_datas)
    warns=MongoHelper.get_alert_warns(hangseng_datas)

    return jsonify({
        "dates":dates,
        "balances":volumes,
        "hongsengIndex":hongsengIndex,
        "ruleEmergCount":[len(x) for x in emergs],
        "ruleEmerg":emergs,
        "ruleWarnCount":[len(x) for x in warns],
        "ruleWarn":warns
    })

@app.route('/report')
def report():
    date=request.args.get("date")
    alert_summart = AlertSummary(date)
    return jsonify(alert_summart.generateSummary())

@app.route('/test')
def test():
    s="数据量附近kjfls计算量凡\"士林是"
    return jsonify(s.decode("utf-8").encode("gbk"))

@app.route('/stock')
def stock():
    return render_template("stock.html")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
