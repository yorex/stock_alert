from flask import Flask
app = Flask(__name__)

import io
import random
import json
import rule_engine
import helper
import logger
from flask import jsonify
from flask import render_template

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
@app.route('/getBalanceHsi')
def get_balance_hsi():
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
        ma5sequences = mahelper.getMa(5, hongsengIndex)
        #engine.add_rule(rule_engine.SequenceMonotonicityRule(app, ma5sequences))
        engine.add_rule(rule_engine.RapidDownRule(app, hongsengIndex, 0.02))
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


@app.route('/stock')
def stock():
    return render_template("stock.html")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
