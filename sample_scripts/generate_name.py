# api 연결

import requests, random
from bs4 import BeautifulSoup

# parse 1)first name and 2)last name
# # load names from url
# url = 'https://raw.githubusercontent.com/kimkkikki/koreanname-frontend/master/static/sitemap.xml'
#
# response = requests.get(url)
# txts = response.text
# # print(txts)
#
# soup = BeautifulSoup(txts,'xml')
#
# names = []
# dlt = 'https://koreanname.me/name/'
# for elm in soup.find_all('url'):
#     name = elm.find('loc').text
#     name = name.replace(dlt, '')
#
#     names.append(name)
#
# names = list(filter(None, names))[5:]
#
# with open('assets/names.txt', 'w', encoding='utf8') as f :
#     for name in names:
#         f.write(name+'\n')
#
# # last name list
# url='http://ko.wikipedia.org/wiki/한국의_성씨'
# response = requests.get(url).text
#
# last_name1, last_name2 = {}, {}
#
# soup = BeautifulSoup(response, 'html.parser')
#
# for tr in soup.find_all('tr'):
#     tds = tr.find_all('td')
#     if len(tds) >= 4 :
#         if tds[0].find('b'):
#             name = tds[0].find('b').get_text()
#
#             if tds[1].get_text() is not None:
#                 freq = tds[1].get_text()
#                 freq = int(freq.replace(',', ''))
#                 if name in last_name1.keys() :
#                     continue
#                 if len(name)==1 :
#                     last_name1[name]=freq
#                 if len(name)==2 :
#                     last_name2[name]=freq
#
# with open('assets/last_names_1.txt', 'w', encoding='utf8') as f :
#     for name,counts in last_name1.items():
#         f.write(name+' '+str(counts)+'\n')
#
# with open('assets/last_names_2.txt', 'w', encoding='utf8') as f :
#     for name,counts in last_name2.items():
#         f.write(name+' '+str(counts)+'\n')



# load names from text

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

if __name__ == '__main__' :
    random_name()