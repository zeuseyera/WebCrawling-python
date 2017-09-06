
#멜론싸이트 크롤링

#자료교환 라이브러리: request
import requests
import json

#-------------------------------------------------------------------------------
#요청할 조건을 설정한다
#url        = "http://www.melon.com/search/keyword/index.json?jscallback=jQuery191033550464676609115_1503740489060&query=%25ED%2585%2581&_=1503740489063"

#웹주소로 요청을 보내고 응답을 받는다
#response = requests.get(url).text

#요청할 조건을 설정한다
JuSo = "http://www.melon.com/search/keyword/index.json"
InSu = {
    'jscallback': 'jQuery191033550464676609115_1503740489060',
    'query': '터보',
    }

#웹주소로 요청을 보내고 응답을 받는다
response = requests.get( JuSo, params=InSu ).text

#받은 자료를 출력한다
print( response )
print( '\n' )

#받은 자료에서 요청한 인수를 삭제한다
json_string = response.replace( InSu['jscallback'] + '(', '' ).replace( ');', '' )
result_dict = json.loads( json_string )

#받은 자료를 출력한다
print( result_dict )
print( '\n' )

print( result_dict['SONGCONTENTS'] )
print( '\n' )

#'SONGCONTENTS'의 개수를 알아낸다
len( result_dict['SONGCONTENTS'] )

#'SONGCONTENTS'의 개수만큼 반복해서 'SONGNAME'을 출력한다
for song in result_dict['SONGCONTENTS']:
    print( song['SONGNAME'] )
print( '\n' )

#'SONGCONTENTS'에서 'SONGNAME', 'ALBUMNAME', 'ARTISTNAME'을 출력한다
for song in result_dict['SONGCONTENTS']:
    print( '{SONGNAME} {ALBUMNAME} {ARTISTNAME}'.format( **song ) )
    #print( song['SONGNAME'], song['ALBUMNAME'], song['ARTISTNAME'] )
print( '\n' )

#'SONGCONTENTS'에서 'SONGNAME', 'ALBUMNAME', 'ARTISTNAME', 주소와 'SONGID'을 출력한다
for song in result_dict['SONGCONTENTS']:
    print( '''{SONGNAME} {ALBUMNAME} {ARTISTNAME}
 - http://www.melon.com/song/detail.htm?songId={SONGID}'''.format( **song ) )
print( '\n' )

#-------------------------------------------------------------------------------
#melon_search 구조정의
def melon_search( Gab ):
    JuSo = "http://www.melon.com/search/keyword/index.json"
    InSu = {
    'jscallback': 'jQuery191033550464676609115_1503740489060',
    'query': Gab,
    }

    #웹주소로 요청을 보내고 응답을 받는다
    response = requests.get( JuSo, params=InSu ).text

    #받은 자료에서 요청한 인수를 삭제한다
    json_string = response.replace( InSu['jscallback'] + '(', '' ).replace( ');', '' )
    result_dict = json.loads( json_string )

    if 'SONGCONTENTS' not in result_dict:
        print( '찾지 못함' )
    else:
        #'SONGCONTENTS'에서 'SONGNAME', 'ALBUMNAME', 'ARTISTNAME', 주소와 'SONGID'을 출력한다
        for song in result_dict['SONGCONTENTS']:
            print( '''{SONGNAME} {ALBUMNAME} {ARTISTNAME}
         - http://www.melon.com/song/detail.htm?songId={SONGID}'''.format( **song ) )
        print( '\n' )

#키보드입력으로 직접 검색
if __name__ == '__main__':
    line = input()
    melon_search( line )

