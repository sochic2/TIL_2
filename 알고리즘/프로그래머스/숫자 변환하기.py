def solution(x, y, n):
    answer = 0
    q = [x]
    while q:
        if y in q:
            return answer
        answer += 1
        new_q = []
        for num in q:
            if num + n <= y:
                new_q.append(num+n)
            if num * 2 <= y:
                new_q.append(num*2)
            if num * 3 <= y:
                new_q.append(num*3)
        q = list(set(new_q))

    return -1


def solution2(x, y, n):
    answer = 0
    visit = [float('inf')] * (y+1)
    visit[x] = 0
    for i in range(x, y+1):
        if visit[i] == float('inf'):continue
        if i+n <= y:
            visit[i+n] = min(visit[i]+1, visit[i+n])
        if i*2 <= y:
            visit[i*2] = min(visit[i]+1, visit[i*2])
        if i*3 <= y:
            visit[i*3] = min(visit[i]+1, visit[i*3])
    if visit[y] == float('inf'):
        return -1
    return visit[y]

a = (10, 40, 5)
# a = (10, 40, 30)
# a = (2, 5, 4)
print(solution(*a))