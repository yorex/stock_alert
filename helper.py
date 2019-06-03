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

if __name__ == '__main__':
    helper = MaHelper()
    print helper.getMa(10, [2,3,4,3,4,2,2,3,5,4,2,2,3,5])
