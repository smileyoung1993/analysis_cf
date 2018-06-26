from itertools import count
from bs4 import BeautifulSoup
import collection.crawler as cw
import pandas as pd
import xml.etree.ElementTree as et
from collection.data_dict import sido_dict,gungu_dict
import urllib
from selenium import webdriver
import time


RESULT_DIRECTORY = '__result__/crawling'
#######################페리카나##########################################
def crawling_pelicana():
    results = []
    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?gu=&si=&page=%d' % page
        html = cw.crawling(url=url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    #store
    table = pd.DataFrame(results, columns=['name','address','sido','gungu'])

    #apply를 통해 lambda함수의 v값이 들어와서 sido를 v로 채움
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

####################네네############################
def proc_nene(xml):
    print('xml:',xml)
    results = []
    root = et.fromstring(xml)
    elements_items = root.findall('item')

    for el in elements_items:
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name,address,sido,gungu,))

    return results


def store_nene(data):
    print('data:',data)
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/nene_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


'''
- paging 처리가 되어야 한다.	
           파라미터 중 sido1, sido2 가 정확하지 않으면 500 오류(HttpError) 가 
           발생 한다.
           따라서  html = crawler.crawling(url=url) 에서 html 이 None인지 확인
           해서 마지막이 지났는 지 검사한다.

'''
##########################교촌#####################################

def crawling_kyochon():
        results = []
        for sido1 in range(1, 18):
            for sido2 in count(start=1):
                try:

                    url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1,sido2)
                    html = cw.crawling(url=url)

                    bs = BeautifulSoup(html, 'html.parser')
                    tag_table = bs.find('div', attrs={'class': 'shopSchList'})
                    # print(tag_table)
                    tags_li = tag_table.findAll('li')
                    # print('tag_tbody:',tag_tbody)
                    #tags_dl = tag_tbody.findAll('dl')
                    for tag_li in tags_li:
                        strings = list(tag_li.strings)
                        print('strings', strings)
                        name = strings[3]
                        address = strings[5]
                        address = address.strip()
                        sidogu = address.split()[:2]
                        results.append((name, address) + tuple(sidogu))

                except:
                    break
            # store
        table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

        # apply를 통해 lambda함수의 v값이 들어와서 sido를 v로 채움
        table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
        table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

        table.to_csv('{0}/kyonchon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)
##################################굽네치킨#########################################
# goobne
def crawling_goobne():
    results = []

    url = 'https://www.goobne.co.kr/store/search_store.jsp'

    # 첫페이지 로딩
    wd = webdriver.Chrome('D:\pychamProjects\chromedriver_win32/chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    for page in count(start=1):
        #자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        time.sleep(5)

        #실행 html (rendering된 html)가져오기
        html = wd.page_source

        #Parsing with bs4
        bs =BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        print('tag_table:',type(tag_tbody),tag_tbody)
        tags_tr = tag_tbody.findAll('tr') # list
        print('tags_tr:',type(tags_tr),tags_tr)

        # 끝 검출
    #     if tags_tr[0].get('class') is None: # tags_tr의 첫번째 문자열이 없을때. 탈출
    #         break
    #     print(tag_tbody)
    #     for tag_tr in tags_tr:
    #         strings = list(tag_tr.strings)
    #         print('strings:', strings)
    #         # print('strings[phonenum]:',type(strings[3]))
    #         name = strings[1]
    #         phoneNum = strings[3]
    #         address = strings[6]
    #         address = address.strip()
    #         sidogu = address.split()[:2]
    #         results.append((name,phoneNum,address) + tuple(sidogu)) # 리스트안에 tuple을 사용하는 이유는 리스트는 내용이 변경될 수 있기때문이다.
    #
    # table = pd.DataFrame(results, columns=['name','phoneNum', 'address', 'sido', 'gungu']) # dictionary 가 아니기 때문에 column명을 정해준다.
    # # apply를 통해 lambda함수의 v값이 들어와서 sido를 v로 채움
    # table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v)) # 첫번째 파라미터의 값이 v, 뒤에 파라미터는 default값 (서울이 sido_dict에 없으면 서울로 default해라)
    # table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
    #
    # table.to_csv('{0}/goobne_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

if __name__ == '__main__':

    #pelicana
    crawling_pelicana()

    # nene
    # cw.crawling(
    #     url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
    #         % (urllib.parse.quote("전체"), urllib.parse.quote("전체")),
    #     proc=proc_nene,
    #     store=store_nene)

    ## 교촌
    #crawling_kyochon()
    ## 굽네
    #crawling_goobne()