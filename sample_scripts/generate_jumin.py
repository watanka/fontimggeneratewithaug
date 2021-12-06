import random

# 주민등록번호 임의 생성기

# jumin ex) '940322 - 1024536' 대쉬 포함
# assert len(jumin) = 16
def random_jumin() :
    def random_ranges(*ranges, digit) :
        all_ranges = sum(ranges, [])
        v = str(random.choice(all_ranges))

        if len(v) < digit :
            return '0'*(digit-len(v)) + v
        else :
            return v

    # year range 1950 ~ 2000, 2000~2020

    year = random_ranges([*range(50,100)], [*range(0, 20)], digit = 2)

    # print('year: {}'.format(year))
    # month 01~12 두 자리 수
    month = random_ranges([*range(1,13)], digit = 2)

    # print('month: {}'.format(month))
    # dates 01~31 두 자리 수

    dates = random_ranges([*range(1,31)], digit = 2)

    # print('dates: {}'.format(dates))

    # sex 1 or 2; 2000년대생 이후로는 3 or 4

    def select_sex(year) :
        if int(year[0]) < 3 :
            return str(random.choice([3,4]))
        else :
            return str(random.choice([1,2]))

    sex = select_sex(year)

    # print('sex: {}'.format(sex))

    # area 00~99
    area = random_ranges([*range(0,100)], digit = 2)

    # print('area: {}'.format(area))
    # 4 digit random number

    last4 = random_ranges([*range(0,9999)], digit = 4)

    # print('last 4: {}'.format(last4))

    # combine altogether

    jumin = year+month+dates+'-'+sex+area+last4

    # print('생성된 주민등록번호: {}'.format(jumin))
    return jumin