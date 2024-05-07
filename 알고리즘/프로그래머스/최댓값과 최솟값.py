def solution(s):
    s = s.split()
    mmin = float('inf')
    mmax = float('-inf')
    for i in s:
        mmin = min(int(i), mmin)
        mmax = max(int(i), mmax)
    return str(mmin) + ' ' + str(mmax)

print(solution('-1 2 -33 4'))