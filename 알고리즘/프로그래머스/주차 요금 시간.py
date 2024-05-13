import math
def solution(fees, records):
    def calculating(fees, spend_time):
        base_time, base_charge, period, period_charge = fees
        if spend_time - base_time < 0:
            return base_charge
        return base_charge + math.ceil((spend_time - base_time)/period) * period_charge

    answer = []
    cars = {}
    max_minutes = 60*23 + 59
    for fee in records:
        hour, car_num, condition = fee.split()
        hour = hour.split(':')
        hour = int(hour[0])*60 + int(hour[1])
        if car_num in cars:
            cars[car_num].append(hour)
        else:
            cars[car_num] = [hour]

    for car, hour in cars.items():
        total_hour = 0
        if len(hour) % 2 == 1:
            total_hour = 23 * 60 + 59

        for i in range(len(hour)-1, -1, -1):
            if i%2 == 1:
                total_hour += hour[i]
            else:
                total_hour -= hour[i]
        total_fee = calculating(fees, total_hour)
        answer.append((car, total_fee))
    answer = sorted(answer)
    answer = [i[1] for i in answer]

    return answer



fees = [180, 5000, 10, 600]
records = ["05:34 5961 IN", "06:00 0000 IN", "06:34 0000 OUT", "07:59 5961 OUT", "07:59 0148 IN", "18:59 0000 IN",
           "19:09 0148 OUT", "22:59 5961 IN", "23:00 5961 OUT"]
print(solution(fees, records))