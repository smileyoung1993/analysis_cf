
import sys
from urllib.request import Request,urlopen
from datetime import datetime

# def error(e):
#     print('%s : %s' % (e,datetime.now()),file = sys.stderr)

# lambda는 마지막결과를 return

def crawling(url = '', encoding ='utf-8',
             err = lambda e:print('%s : %s' % (e,datetime.now()),file = sys.stderr),
             proc = lambda html:html,
             store = lambda html:html):
            # lambda 로 default 값을 html로 해서 함수가 없을 경우 사용
    try:
        request = Request(url)
        result = urlopen(request)

        try:
            receive = result.read()
            result = store(proc(receive.decode(encoding)))
            # store에는 proc의 결과 list가 가고, proc에는 요청한 url를 읽어온 xml이 들어간다.

            # encoding한 html를 proc에 넣고, store에 저장
        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace') # 사이트마다 utf-8을 이상하게 한곳이있어서 replace를 통해 2번한다.
        #print('%s: success for request [%s]' % (datetime.now(),url))
        return result

    except Exception as e:
        err(e)
        #print('%s : %s' % (e,datetime.now()),file = sys.stderr)
