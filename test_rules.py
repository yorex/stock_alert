import sys
import rule_engine
import pytest

def test_sequence_monotonicity_rule():
    sequences = ['-', '-', '-', '-', 28910, 
                28793, 28702.074, 28693.92, 28647.89, 28662.2, 
                28819, 29000, 29109.2, 29211.9, 29256.0, 
                29276.2, 29099.1, 28919, 28800, 28741, 
                28729, 28936, 29220.6, 29498.9]

    upCount=[0,0,0,0,0,
         0,0,0,0,0,
         1,1,1,1,1,
         1,0,0,0,0,
         0,0,1,1]

    downCount=[0,0,0,0,0,
           0,1,1,1,0,
           0,0,0,0,0,
           0,0,1,1,1,
           1,0,0,0]

    engine = rule_engine.RuleEngine(None)
    engine.add_rule(rule_engine.SequenceMonotonicityRule(None, sequences))
    alerts = engine.inspect()

    warnAlerts = alerts[rule_engine.WARN]
    assert len(upCount) == len(warnAlerts)
    for i in range(len(upCount)):
        assert upCount[i] == len(warnAlerts[i])
    
    emergAlerts = alerts[rule_engine.EMERG]
    assert len(downCount) == len(emergAlerts)
    for i in range(len(downCount)):
        assert downCount[i] == len(emergAlerts[i])


def test_rapid_down_rule():
     sequences = [ 28793, 28702.074, 28693.92, 28647.89, 28662.2, 
                28729, 28936, 29220.6, 29498.9]

    downCount=[0,0,0,0,0,
           1,0,0,0]

    engine = rule_engine.RuleEngine(None)
    engine.add_rule(rule_engine.RapidDownRule(None, sequences, 0.02))
    alerts = engine.inspect()

    emergAlerts = alerts[rule_engine.EMERG]
    assert len(downCount) == len(emergAlerts)
    for i in range(len(downCount)):
        assert downCount[i] == len(emergAlerts[i])

if __name__ == "__main__":
    pytest.main(['-s', 'test_rules.py'])
