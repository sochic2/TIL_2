def solution(order):
    answer = 0
    order_idx = 0
    container_num = 1
    stack = []

    while True:
        if container_num > len(order)+1:
            return answer
        if container_num > len(order) and len(stack) == 0:
            return answer
        order_num = order[order_idx]
        if container_num == order_num:
            answer += 1
            order_idx += 1
            container_num += 1
        elif len(stack) > 0 and stack[-1] == order_num:
            answer += 1
            order_idx += 1
            stack.pop(-1)
        elif container_num != order_num and (len(stack) == 0 or stack[-1] != order_num):
            stack.append(container_num)
            container_num += 1

    return answer



order = [4, 3, 1, 2, 5]
# order = [5, 4, 3, 2, 1]

print(solution(order))