def solution(s):
    s = s.split(' ')
    print(s)
    result = []
    for word in s:
        if len(word) > 1:
            result.append(word[0].upper() + word[1:].lower())
        elif len(word) == 1:
            result.append(word[0].upper())
        else:
            result.append('')
    answer = ' '.join(result)
    return answer

## title() 이란 함수 있대

# s = "3people unFollowe?d me"
s = "for the   3last wEek"
print(solution(s))
