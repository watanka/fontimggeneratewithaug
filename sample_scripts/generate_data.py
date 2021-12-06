import random

# generate info -> customize generate function suited for data subjects
def random_address():
    with open('../assets/address.json', encoding='utf8') as f :
        adrs_dict = json.load(f)

    do = random.choice(list(adrs_dict.keys()))
    gu = random.choice(list(adrs_dict[do].keys()))
    dong = random.choice(adrs_dict[do][gu])

    return ' '.join([do,gu,dong]).replace('  ', ' ')

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

def random_name():
    with open('../assets/last_names_1.txt', 'r', encoding='utf8') as f:
        data = f.read().split('\n')
        sung, freq= zip(*[(d.split(' ')) for d in data])

        freq= [int(f) for f in freq]
        total = sum(freq)
        freq= [f/total for f in freq]

        last_name = random.choices(sung, freq)[0]

    with open('../assets/names.txt', 'r', encoding='utf8') as f:
        data = f.read().split('\n')
        first_name = random.choice(data)

    name = last_name+first_name
    # print('생성된 이름 : {}'.format(name))

    return name

def random_gen( data_opts=['jumin', 'name', 'address']) :
    draw_txt=[]
    if 'jumin' in data_opts:
        jumin=random_jumin()
        draw_txt.append(jumin)
    if 'name' in data_opts:
        name=random_name()
        draw_txt.append(name)
    if 'address' in data_opts :
        adrss=random_address()
        draw_txt.append(adrss)

    draw_txt = ' '.join(draw_txt)

    return draw_txt

if __name__=='__main__':
    pass