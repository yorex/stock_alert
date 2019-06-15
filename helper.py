import sys


class MaHelper:
    # n: ma{n}
    def getMa(self, n, arr):
        ma=[]
        if not arr:
            return ma
        for i in range(len(arr)):
            if i < n-1:
                ma.append('-')
            else:
                ma.append(sum(arr[i-n+1:i+1])*1.0/n)
        return ma

    def test(self):
        ai=[11.28, 11.47, 11.53, 11.07, 11.58, 11.52, 10.98, 10.23, 10.56, 9.75]
        print ai
        ma5_lable=['-','-','-','-',86.139, 78.187, 65.542, 52.95, 45.845, 37.943]
        ma5 = self.getMa(5, ai) 
        print ma5
        

if __name__ == '__main__':
    helper = MaHelper()
    print helper.getMa(10, [2,3,4,3,4,2,2,3,5,4,2,2,3,5])
