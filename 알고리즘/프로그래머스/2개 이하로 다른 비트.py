def solution(numbers):
    answer = []
    for num in numbers:
        if num % 2 == 0:
            answer.append(num + 1)
        else:
            convert_num = []
            while num > 1:
                convert_num.append(num % 2)
                num //= 2
            convert_num.append(num)
            convert_num.reverse()
            convert_num = [0] + convert_num

            print('convert_num', convert_num)

            result_idx = float('inf')
            for idx, num in enumerate(convert_num):
                if num == 0:
                    result_idx = idx
            result_double = convert_num[:result_idx] + [1, 0] + convert_num[result_idx+2:]
            result_num = 0
            start = 1
            print(result_double)
            for i in range(len(result_double)-1, -1, -1):
                result_num += start * result_double[i]
                start *= 2
            answer.append(result_num)

    return answer

print(solution([2, 11]))