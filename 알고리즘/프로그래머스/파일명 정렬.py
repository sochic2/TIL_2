def solution(files):
    answer = []
    for file in files:
        for idx, cha in enumerate(file):
            if cha.isdigit():
                header = file[:idx]
                header_idx = idx
                num = ''
                for idx, n in enumerate(file[header_idx:]):
                    if not n.isdigit():
                        num = file[header_idx:header_idx+idx]
                        num_idx = idx + header_idx
                        break
                if num == '':
                    num = file[header_idx:]
                    answer.append((header, num, ''))
                else:
                    answer.append((header, num, file[num_idx:]))
                break
    print(answer)
    answer = sorted(answer, key= lambda x: (x[0].lower(), int(x[1])))
    answer = [''.join(i) for i in answer]
    return answer

files = ["img10000t", "img12.png", "img02t.png", "img1.png", "IMG01.GIF", "img2.JPG"]

print(solution(files))