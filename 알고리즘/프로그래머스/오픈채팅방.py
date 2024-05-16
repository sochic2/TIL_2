def solution(record):
    answer = []
    user = {}
    for para in record:
        if para[0] == 'L':
            pass
        else:
            status, uid, nick_name = para.split()
            user[uid] = nick_name

    for para in record:
        if para[0] == 'L':
            status, uid = para.split()
            nick_name = user[uid]
            answer.append(f'{nick_name}님이 나갔습니다.')

        if para[0] == 'E':
            status, uid, _ = para.split()
            nick_name = user[uid]
            answer.append(f'{nick_name}님이 들어왔습니다.')

    return answer


record = ["Enter uid1234 Muzi", "Enter uid4567 Prodo","Leave uid1234","Enter uid1234 Prodo","Change uid4567 Ryan"]
print(solution(record))