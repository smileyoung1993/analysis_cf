from bs4 import BeautifulSoup

html = '<td class="title"><div class="tit3">'\
        '<a href="/movie/bi/mi/basic.nhn?code=120160"'\
        'title="미이라">미이라</a></div></td>'


# 1. tag 조회
# ?? tag 역할
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    print(bs)
    # parser는 숲 --> 나무
    tag = bs.td
    print(tag.name)

    tag = bs.td
    print(tag.div)

# attribute 값
def ex2():
    bs = BeautifulSoup(html,'html.parser')

    tag = bs.td
    print(tag['class'])

    tag = bs.div
    #없으면 에러
    #print(tag['id'])
    print(tag.attrs)
# attributes 조회
def ex3():
    bs = BeautifulSoup(html,'html.parser')

    tag = bs.find('td',attrs={'class':'title'})
#    print(tag)

    tag = bs.find(attrs={'class':'tit3'})
    print(tag)




if __name__ == '__main__':
    #ex1()
    #ex2()
    ex3()