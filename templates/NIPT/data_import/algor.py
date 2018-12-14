class Solution(object):
    def largestTimeFromDigits(self, A):
        """
        :type A: List[int]
        :rtype: str
        """
        def permute(num):
            if len(num) == 0: return []
            if len(num) == 1: return [num]
            res = []
            for i in range(len(num)):
                x  = num[i]
                xs = num[:i] + num[i+1:]
                for j in permute(xs):
                    res.append([x] + j)
            return res
        permu = permute(A)
        cur_max = -1
        res = []
        for per in permu:
            if 0 <= per[0] * 10 + per[1] <= 23:
                if 0 <= per[2] * 10 + per[3] <= 59:
                    if (per[0] * 10 + per[1]) * 60 + per[2] * 10 + per[3] > cur_max:
                        cur_max = (per[0] * 10 + per[1]) * 60 + per[2] * 10 + per[3]
                        res = per
        if cur_max == -1:
            return ''
        return ''.join(str(i) for i in res)[:2] + ':' + ''.join(str(i) for i in res)[2:]

A = [2,1,5,3]
B = Solution()
print(B.largestTimeFromDigits(A))

C = [4,2,3]
C.sort()
print(C)
