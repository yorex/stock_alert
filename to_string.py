#coding=utf8

class ToString:
    def __init__(self, coding, indent=2):
        self.coding = coding
        self.indent = indent

    def stringList(self, lst):
        ls="["
        first=True
        for item in lst:
            if not first:
                ls+=","
            ls+=self.toString(item)
            first=False
        ls+="]"
        return ls

    def stringDict(self, dct):
        ds="{"
        first=True
        for k in dct:
            if not first:
                ds+=","
            ds+=self.toString(k)
            ds+=":"
            ds+=self.toString(dct[k])
            first=False
        ds+="}"
        return ds

    def stringUnicode(self, uni):
        if uni:
            return '"'+uni.encode(self.coding)+'"'
        else:
            return ""

    def stringTuple(self, tple):
        pass

    def stringStr(self, ss):
        if ss:
            return '"'+ss+'"'
        else:
            return ""

    def toString(self, o):
        s=""
        if isinstance(o, list):
            s+=self.stringList(o)
        elif isinstance(o, dict):
            s+=self.stringDict(o)
        elif isinstance(o, unicode):
            s+=self.stringUnicode(o)
        elif isinstance(o, str):
            s+=self.stringStr(o)
        elif isinstance(o, tuple):
            s+=self.stringTuple(o)
        return s
