#===============================================================================
#
# Python 3.5
# requests
# beautifulsoup4
# datetime

#-------------------------------------------------------------------------------
# requests 라이브러리를 탑재한다
import requests

# 자료를 받아올 주소를 설정한다
WebJuSo = "https://okky.kr/articles/questions"

# 설정한 주소에서 자료를 수집한다
SuSinJaRyo = requests.get( WebJuSo )

# 수집한 자료를 화면에 출력한다
print( SuSinJaRyo.text )

#-------------------------------------------------------------------------------
# BeautifulSoup4 라이브러리를 탑재한다
# 반드시 bs4 => BeautifulSoup 로 불러온다
from bs4 import BeautifulSoup

# 수신자료에 분석기를 덧붙인다
BunSeogGi = BeautifulSoup( SuSinJaRyo.text, 'html.parser' )

# 분석기에서 추출할 자료의 목록 양식을 지정한다
# <li class="list-group-item list-group-item-question list-group-no-note clearfix"> 에서
# li 클래스의 list-group-item 을 선택하는 기준으로 설정하고, 설정한 클래스를 배열에 복사한다
SeonTaeg = BunSeogGi.select( 'li.list-group-item' )

SeonTaeg0 = SeonTaeg[0]
print( SeonTaeg0, '\n' )

# <h5 clas> 와 <a href> 가 일치하는 영역을 지정한다
# MogRog 에서 추출할 내용의 선택기준을 설정하고, 설정한 내용을 복사한다
JiJeong = SeonTaeg0.find( 'h5' ).select_one( 'a' )
print( JiJeong, '\n' )

# JiJeong 에서 연결주소를 추출한다
link = JiJeong[ 'href' ]
print( link, '\n' )

# link 에서 목록번호를 추출한다
# split( '/' )[-1] => '/' 로 분리 했을때 맨 뒤에서 첫번째(-1) 
BeonHo = link.split( '/' )[-1]
print( BeonHo, '\n' )

# JiJeong 에서 제목을 추출한다
#JeMog = JiJeong.text
# JiJeong 에서 제목의 공백을 제거하고 제목을 추출한다
JeMog = JiJeong.text.strip()
print( JeMog, '\n' )

#-------------------------------------------------------------------------------
# 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
from datetime import datetime

# 수집한 자료를 저장할 파일이름을 설정한다
# 파일이름에 ':'(콜론)을 사용하면 안된다( 왜 그런가 ??? )
FileMyoung = datetime.strftime( datetime.now(), "./SuJib_%Y-%m-%d_%Hh%Mm%Ss.txt" )

# 파일이름의 파일을 연다( 쓰기모드, utf-8 옵션 )
File = open( FileMyoung, 'w', encoding='utf-8' )
#File = open( datetime.strftime( datetime.now(), "./SuJib_%Y-%m-%d_%Hh%Mm%Ss.txt" ), 'w', encoding='utf-8' )

# 선택한 전체자료를 반복해서 수집자료를 추출하여 파일로 저장한다
data = '연결, 번호, 제목\n'

for BanBog in SeonTaeg:
    JiJeong = BanBog.find( 'h5' ).select_one( 'a' )
    link = JiJeong[ 'href' ]
    BeonHo = link.split( '/' )[-1]
    JeMog = JiJeong.text.strip()

    print( link, BeonHo, JeMog, '\n' )

    data = '%s, %s, %s\n' %( link, BeonHo, JeMog )
    File.write( data )

# 파일을 닫는다
File.close()



