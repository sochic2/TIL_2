def solution(skill, skill_trees):
    answer = 0
    for tree in skill_trees:
        idx = 0
        flag = 0
        for i in tree:
            if flag == 1:
                break
            if i in skill:
                if i == skill[idx]:
                    idx += 1
                else:
                    flag = 1
        if flag == 0:
            answer += 1

    return answer



skill = "CBD"
skill_trees = ["BACDE", "CBADF", "AECB", "BDA"]
print(solution(skill, skill_trees))