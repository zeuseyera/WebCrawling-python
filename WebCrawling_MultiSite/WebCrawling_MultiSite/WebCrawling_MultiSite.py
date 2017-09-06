#===============================================================================
# 
# Python 3.5
# requests
# beautifulsoup4
# datetime

#===============================================================================
# 여러주소에서 자료를 수집한다
#
# https://okky.kr/articles/questions
# https://okky.kr/articles/tech
# https://okky.kr/articles/community
# https://okky.kr/articles/columns
#
# http://www.todayhumor.co.kr/board/list.php?table=programmer
# http://www.todayhumor.co.kr/board/list.php?table=it
#
# https://qna.iamprogrammer.io

#-------------------------------------------------------------------------------
# requests 라이브러리를 탑재한다
import requests
# BeautifulSoup4 라이브러리를 탑재한다
# 반드시 bs4 => BeautifulSoup 로 불러온다
from bs4 import BeautifulSoup
# urllib, lrllib.parse 라이브러리를 urlparse로 불러온다
import urllib
from urllib.parse import urlparse

from datetime import datetime

# 주기적으로 반복실행을 하기 위해 apscheduler 라이브러리를 불러온다
import os
from apscheduler.schedulers.blocking import BlockingScheduler

# 주소목록 설정
JuSo = [
    'https://okky.kr/articles/questions',
    'https://okky.kr/articles/tech',
    'https://okky.kr/articles/community',
    'https://okky.kr/articles/columns',

    'http://www.todayhumor.co.kr/board/list.php?table=programmer',
    'http://www.todayhumor.co.kr/board/list.php?table=it',
    
    'https://qna.iamprogrammer.io',

    'https://www.ppomppu.co.kr/zboard/zboard.php?id=developer&page=1'
]

#-------------------------------------------------------------------------------
# 포코분석기 정의
class PokoBunSeogGi:
    
    def __init__( self, func=None ):
        if func:
            self.BunSeog_JuSo = func
            
    def BunSeog_JuSo( self, _JuSo ):
        print( "구현이 안됐어요~..." )
        print( _JuSo )

#-------------------------------------------------------------------------------
# 오키분석기 정의
def BunSeogGi_okky( _JuSo ):
    WebJuSo = _JuSo                         # 자료를 받아올 주소를 설정한다
    SuSinJaRyo = requests.get( WebJuSo )    # 설정한 주소에서 자료를 수집한다

    # 수신자료에 분석기를 덧붙인다
    BunSeogGi = BeautifulSoup( SuSinJaRyo.text, 'html.parser' )

    # 분석기에서 추출할 자료의 목록 양식을 지정한다
    # <li class="list-group-item list-group-item-question list-group-no-note clearfix"> 에서
    # li 클래스의 list-group-item 을 선택하는 기준으로 설정하고, 설정한 클래스를 배열에 복사한다
    MogRog = BunSeogGi.select( 'li.list-group-item' )

    # 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
    data = ''

    for BanBog in MogRog:
        # <h5 clas> 와 <a href> 가 일치하는 영역을 지정한다
        # MogRog 에서 추출할 내용의 선택기준을 설정하고, 설정한 내용을 복사한다
        JiJeong = BanBog.find( 'h5' ).select_one( 'a' )
        # JiJeong 에서 연결주소를 추출한다
        link = JiJeong[ 'href' ]
        # link 에서 목록번호를 추출한다
        # split( '/' )[-1] => '/' 로 분리 했을때 맨 뒤에서 첫번째(-1) 
        BeonHo = link.split( '/' )[-1]
        # JiJeong 에서 제목을 추출한다
        #JeMog = JiJeong.text
        # JiJeong 에서 제목의 공백을 제거하고 제목을 추출한다
        JeMog = JiJeong.text.strip()

        #print( link, BeonHo, JeMog, '\n' )
        data += '%s, %s, %s\n' %( link, BeonHo, JeMog )

    return data

#-------------------------------------------------------------------------------
# todayhumor 분석기를 정의한다
def BunSeogGi_todayhumor( _JuSo ):
    WebJuSo = _JuSo                         # 자료를 받아올 주소를 설정한다
    SuSinJaRyo = requests.get( WebJuSo )    # 설정한 주소에서 자료를 수집한다

    # 수신자료에 분석기를 덧붙인다
    BunSeogGi = BeautifulSoup( SuSinJaRyo.text, 'html.parser' )

    # 분석기에서 추출할 자료의 목록 양식을 지정한다
    # <tr class="view list_tr_programmer" mn="715588"> 에서
    # tr 크래스의 view 를 선택기준으로 설정
    MogRog = BunSeogGi.select( 'tr.view' )

    # 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
    data = ''

    for BanBog in MogRog:
        # <td class="no"><a href 에서, td 클래스 "no" 의 a를 지정
        JiJeong = BanBog.select_one( 'td.no a' )
        # 지정에서 연결주소를 추출한다
        link = JiJeong[ 'href' ]
        # 지정에서 목록번호를 추출한다
        BeonHo = JiJeong.text
        # <td class="subject"><a href 에서, 제목을 추출한다
        JeMog = BanBog.select_one( 'td.subject a' ).text

        #print( link, BeonHo, JeMog, '\n' )
        data += '%s, %s, %s\n' %( link, BeonHo, JeMog )

    return data

#-------------------------------------------------------------------------------
# geturi 정의
def get_uri( _JuSo ):
    return urlparse( _JuSo )[ 0 ] + '://' + urlparse( _JuSo )[ 1 ]

#-------------------------------------------------------------------------------
# iamprogrammer 분석기를 정의한다
def BunSeogGi_iamprogrammer( _JuSo ):
    WebJuSo = _JuSo                         # 자료를 받아올 주소를 설정한다
    SuSinJaRyo = requests.get( WebJuSo )    # 설정한 주소에서 자료를 수집한다

    # 수신자료에 분석기를 덧붙인다
    BunSeogGi = BeautifulSoup( SuSinJaRyo.text, 'html.parser' )

    # 분석기에서 추출할 자료의 목록 양식을 지정한다
    # <div class="contents"><table id="ember1482" class="ember-view topic-list"> 에서
    # div 크래스의 topic-list 를 선택기준으로 설정
    SeonTaeg = BunSeogGi.select_one( 'div.topic-list' )
    # 'div', { 'itemprop': 'itemListElement' } 모든 목록을 찾는다
    MogRog = SeonTaeg.find_all( 'div', { 'itemprop': 'itemListElement' } )

    # 처음 1개는 공지다, 제일처음 목록을 삭제한다
    MogRog = MogRog[ 1: ]

    # 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
    data = ''

    for BanBog in MogRog:
        # 주소와 목록에서 연결주소를 추출한다
        link = get_uri( _JuSo ) + BanBog.select_one( 'a' )[ 'href' ]
        # 연결에서 목록번호를 추출한다
        BeonHo = link.split( '/' )[ -1 ]
        # <'span', { 'itemprop': 'name' } 에서, 제목을 추출한다
        JeMog = BanBog.find( 'span', { 'itemprop': 'name' } ).text

        #print( link, BeonHo, JeMog, '\n' )
        data += '%s, %s, %s\n' %( link, BeonHo, JeMog )

    return data

BunSeogGi_SeonTaeg_MogRog = {
    'okky.kr': BunSeogGi_okky,
    'www.todayhumor.co.kr': BunSeogGi_todayhumor,
    'qna.iamprogrammer.io': BunSeogGi_iamprogrammer,
    #'www.ppomppu.co.kr': BunSeogGi_ppomppu,
}

#-------------------------------------------------------------------------------
# 주소를 반복해서 분석기를 호출하여 자료를 수집한다
def scraping():
    # 수집한 자료를 저장할 파일이름을 설정한다
    # 파일이름에 ':'(콜론)을 사용하면 안된다( 왜 그런가 ??? )
    FileMyoung = datetime.strftime( datetime.now(), "./SuJib_%Y-%m-%d_%Hh%Mm%Ss.txt" )

    # 파일이름의 파일을 연다( 쓰기모드, utf-8 옵션 )
    fo = open( FileMyoung, 'w', encoding='utf-8' )
    #File = open( datetime.strftime( datetime.now(), "./SuJib_%Y-%m-%d_%Hh%Mm%Ss.txt" ), 'w', encoding='utf-8' )

    # 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
    #data = '연결, 번호, 제목\n'
    fo.write( '연결, 번호, 제목\n' )

    for BanBog in JuSo:
        #urllib의 parse 로 주소를 분석한다
        SeonTaeg_JuSo = urlparse( BanBog )
    
        # 주소별로 사용할 분석기를 선택해서 넣어준다
        # SeonTaeg_JuSo[0] => 프로토콜, SeonTaeg_JuSo[1] => 도메인주소
        print( "=====================================================" )
        print( "[선택한 분석기] %s" % SeonTaeg_JuSo[ 1 ] )
        print( "=====================================================" )
        fo.write( "=====================================================\n" )
        fo.write( "[선택한 분석기] %s\n" % SeonTaeg_JuSo[ 1 ] )
        fo.write( "=====================================================\n" )

        # 분석기 함수를 받는다
        try:
            GiNeung = BunSeogGi_SeonTaeg_MogRog[ SeonTaeg_JuSo[ 1 ] ]
            # 선택한 분석기를 포코분석기로 전달한다
            BunSeogGi = PokoBunSeogGi( GiNeung )
            # 포분석기에 분석할 주소를 설정한다
            #BunSeogGi.BunSeog_JuSo( BanBog )
            SuJibGab = BunSeogGi.BunSeog_JuSo( BanBog )
            print( SuJibGab )
            fo.write( SuJibGab )

        except KeyError as e:
            print( '이 주소는 분석기를 만들어야 해요~ 개발자님...', e )

    # 파일을 닫는다
    fo.close()

#-------------------------------------------------------------------------------
# 주기적으로 반복실행을 한다

if __name__ == '__main__':
    # 스케쥴러를 할당한다
    scheduler = BlockingScheduler()

    print( "스케줄러 시작!" )

    scheduler.add_job( scraping, 'interval', seconds=30 )

    try:
        scheduler.start()
    except( KeyboardInterrupt, SystemExit ):
        print( "스케쥴러를 종료했음." )
        pass


