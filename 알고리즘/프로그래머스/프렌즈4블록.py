def board_move(m, n, board):
    for y in range(m-1, -1, -1):
        for x in range(n):
            if board[y][x] == 0:
                new_y = y
                while True:
                    new_y -= 1
                    if new_y == -1:
                        break
                    if board[new_y][x] != 0:
                        board[y][x], board[new_y][x] = board[new_y][x], board[y][x]
                        break
    return board


def solution(m, n, board):
    board = [[word for word in char] for char in board]
    answer = 0
    while True:
        to_remove = []
        directions = [(0, 1), (1, 0), (1, 1)]
        for y in range(m):
            for x in range(n):
                cha = board[y][x]
                if cha == 0:continue
                candi = [(y, x)]
                for dy, dx in directions:
                    new_y, new_x = y + dy, x + dx
                    if new_y > m-1 or new_x > n-1:
                        break
                    if cha != board[new_y][new_x]:
                        break
                    else:
                        candi.append((new_y, new_x))

                if len(candi) == 4:
                    to_remove += candi
        if len(to_remove) == 0:
            break
        a = 1
        to_remove = list(set(to_remove))
        answer += len(to_remove)
        for y, x in to_remove:
            board[y][x] = 0
        board = board_move(m, n, board)
        for i in board:
            for j in i:
                print(j, end='')
            print()
        print()
    return answer


m, n, board = 4, 5, ["CCBDE"
                   , "AAADE"
                   , "AAABF"
                   , "CCBBF"]

m, n, board = 6, 6, [
                    "TTTANT",
                    "RRFACC",
                    "RRRFCC",
                    "TRRRAA",
                    "TTMMMF",
                    "TMMTTJ"]
print(solution(m, n, board))
