def solution(topping):
    answer = 0
    charles = [0] * 10001
    brother = [0] * 10001
    charles_topping = 0
    brother_topping = 0
    for top in topping:
        if charles[top] == 0:
            charles_topping += 1
        charles[top] += 1

    for top in topping:
        charles[top] -= 1
        if charles[top] == 0:
            charles_topping -= 1
        brother[top] += 1
        if brother[top] == 1:
            brother_topping += 1
        if brother_topping == charles_topping:
            answer += 1

    return answer



topping = [1, 2, 1, 3, 1, 4, 1, 2]
print(solution(topping))