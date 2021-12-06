# 2020.01월분 자료임 -> TODO : 전체 자료로 확장

import random,json
from collections import defaultdict

#parse address
# do = ['강원도', '경기도', '경상남도', '경상북도',
#       '광주광역시', '대구광역시','대전광역시','부산광역시',
#       '서울특별시','세종특별자치시', '울산광역시', '인천광역시',
#       '전라남도', '전라북도', '제주특별자치도', '충청남도', '충청북도'
#       ]
#
# # ex) 텍스트 정보 형식
# '''
# 1111010100100010000030843|1|1111010100|서울특별시|종로구|청운동||0|1|0|1
# 1111010100100040007031419|3|1111010100|서울특별시|종로구|청운동||0|4|11|0
# 1156013300109640010005607|15|1156013300|서울특별시|영등포구|대림동||0|964|11|0
# 5,6번째만 추출
# '''
# # parse info
#
# adrs_dict = dict()
#
# file_path = 'assets/address/지번_'
# for d in do :
#     adrs_dict[d] = {}
#     txtfile = file_path+d+'.txt'
#
#     with open(txtfile) as f :
#         data = f.read().split('\n')
#         adrs_dict[d] = defaultdict(set)
#         for dat in data:
#             if dat == '':
#                 continue
#             loc, sub_loc = dat.split('|')[4:6]
#             adrs_dict[d][loc].add(sub_loc)
#
# adrs_dict = dict(adrs_dict)
#
# for do, add in adrs_dict.items():
#     for gu, dong in add.items():
#         adrs_dict[do][gu] = list(dong)
#
#
#
#
# with open('assets/address.json', 'w', encoding='utf-8') as f :
#     json.dump(adrs_dict,f,ensure_ascii=False, indent=4)




def random_address():
    with open('../assets/address.json', encoding='utf8') as f :
        adrs_dict = json.load(f)

    do = random.choice(list(adrs_dict.keys()))
    gu = random.choice(list(adrs_dict[do].keys()))
    dong = random.choice(adrs_dict[do][gu])

    return ' '.join([do,gu,dong]).replace('  ', ' ')

if __name__=='__main__':
    random_address()