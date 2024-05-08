def solution(numbers):
    answer = [-1] * len(numbers)
    stack = []
    for idx, num in enumerate(numbers):
        while True:
            if len(stack) == 0:
                stack.append((idx, num))
                break
            stack_idx, stack_num = stack[-1]
            if stack_num < num:
                answer[stack_idx] = num
                stack.pop(-1)
            else:
                stack.append((idx, num))
                break
    return answer

print(solution([9, 1, 5, 3, 6, 2]))
# print(solution([2, 3, 3, 5]))