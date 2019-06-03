from flask import Flask
app = Flask(__name__)

import io
import random
import json
import rule_engine
from flask import jsonify
from flask import render_template

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
@app.route('/getBalance')
def get_balance():
    with open('static/data/balance.dat', 'r') as fp:
        dates=[]
        balances=[]
        hongsengIndex=[]
        for line in fp:
            if not line or len(line)==0: 
                continue
            items = line.strip().split("|")
            dates.append(items[0])
            balances.append(int(items[1]))
            hongsengIndex.append(10000)
#            ruleEmerg.append(items[2:3])
#            ruleEmergCount.append(1 if len(items[2])>0 else 0)
#            ruleWarn.append(items[3:4])
#            ruleWarnCount.append(1 if len(items[3])>0 else 0)
        rule_engine = RuleEngine(DT_BALANCES=balances)
        alerts = rule_engine.inspect()

        return jsonify({
            "dates":dates,
            "balances":balances,
            "hongsengIndex":hongsengIndex,
            "ruleEmergCount":[len(x) for x in alerts[EMERG]],
            "ruleEmerg":alerts[EMERG],
            "ruleWarnCount":[],
            "ruleWarn":[len(x) for x in alerts[WARN]]
        })


@app.route('/stock')
def stock():
    return render_template("stock.html")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
