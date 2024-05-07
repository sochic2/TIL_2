def solution(s):
    answer = True
    stack = []
    for i in s:
        if i == '(':
            stack.append('(')
        else:
            if len(stack) > 0:
                stack.pop()
            else:
                answer = False
    if len(stack) > 0:
        answer = False
    return answer


print(solution("(())()"))

