def solution(land):
    answer = 0
    for row in range(1, len(land)):
        for column in range(4):
            max_candi = max(land[row-1][:column] + land[row-1][column+1:])
            land[row][column] = max_candi + land[row][column]

    return max(land[len(land)-1])

# 해설
# 2번쨰 row각 column이 최대값이 될 수 있는 경우를 생각한다. 본인과 같은 칸이 아닌 것 중 최대를 취할수 있다. 이렇게 되면 두번쨰줄의 각 칸이 취할 수 있는
# 최대 값을 구할 수 있다. 그리고 3번쨰 줄로 넘어간다.
# 3번쨰 줄에서도 1, 2번째 줄을 거치며 각 자리에서 취할 수 있는 윗줄의 최대값과 각 칸의 합을 구할 수 있다. 만약 DP로 풀지 않았다면 완탐을 통해 거미줄처럼
# 뻗어나갔어야 할 것이다. 하지만 DP로 해결했기에 각 자리에서 취할수 있는 이전 줄들의 값들의 합을 바로 윗줄만 보고도 알 수 있는 것이다.
# 즉, land[a][b]가 취할 수 있는 0~a-1번쨰 줄까지의 값은 각 row를 거쳐오며 최대값들을 찾아봤던 바로 윗줄 한줄만 확인하면 된다.


land = [[1,2,3,5],[5,6,7,8],[4,3,2,1]]
print(solution(land))


