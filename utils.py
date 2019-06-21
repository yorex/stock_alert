import sys

def compare_array(ax, ay):
    if len(ax) != len(ay):
        return False 
    for i in range(len(ax)):
        if type(ax[i]) != type(ay[i]):
            return False
        if isinstance(ax[i], float):
            if abs(ax[i]-ay[i]) > 0.001:
                return False
        elif ax[i] != ay[i]:
            return False
    return True
