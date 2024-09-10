import os
from PublicDataReader import TransactionPrice
import PublicDataReader as pdr
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

service_key = os.environ.get("API_KEY")

api = TransactionPrice(service_key)

#시군구 코드 조회

def sigungu_code(addr):
    sido_name = addr[0]
    road_name = ""
    address_link  = {
        '경남' : '경상남도',
        '충북' : '충청북도',
        '충남' : '충청남도',
        '전남' : '전라남도',
        '전북' : '전라북도',
        '경북' : '경상북도',
    }

    if sido_name in address_link:
        sido_name = address_link[sido_name]
        sigungu_name = addr[2]
        road_name = addr[3] +addr[4]
        
        code = pdr.code_bdong()
        df = code.loc[(code['시도명'].str.contains(sido_name)) & (code['시군구명'].str.contains(sigungu_name)) &
            (code['읍면동명']=='')]
        result = df['시군구코드'].tolist()
    
    else:
        sido_name = addr[0]
        sigungu_name = addr[1]
        road_name = addr[2] + addr[3]
        code = pdr.code_bdong()
        df = code.loc[(code['시도명'].str.contains(sido_name)) & (code['시군구명'].str.contains(sigungu_name)) &
            (code['읍면동명']=='')]
        result = df['시군구코드'].tolist()

    
    if len(result) >= 2:
        return result[1], road_name
    else:
        return result[0] , road_name
     
    
def search_apt_price(type, sigungu_code, start_year_month, end_year_month):
    # 기간 내 조회
    df = api.get_data(
        property_type=type,
        trade_type="매매",
        sigungu_code=sigungu_code,
        start_year_month=start_year_month,
        end_year_month=end_year_month,
    )
    
    #원하는 column만 출력되도록 조정
    df = df[["roadNm","aptNm","excluUseAr","dealYear","dealMonth","dealDay","dealAmount","floor",
         "buildYear","dealingGbn","aptDong"]]
    # column을 한글 이름으로 변경
    df = df.rename(columns = {"roadNm": "도로명" , "aptNm":"단지명", "excluUseAr":"전용면적", "dealYear":"계약년도",
                          "dealMonth":"계약월","dealDay":"계약일","dealAmount":"거래금액(단위:만원)","floor":"층",
                          "buildYear":"건축년도","dealingGbn":"거래유형","aptDong":"아파트동",})
    # column을 원하는 위치로 재배치
    df = df[["단지명","아파트동","층","전용면적","도로명","계약년도","계약월","계약일","거래금액(단위:만원)","거래유형","건축년도"]]
    
    return df.head(10)



if __name__ == "__main__":
    sigungu_code = sigungu_code('부산', '강서구')

    print(sigungu_code)

    apt_price = search_apt_price('아파트',sigungu_code,'202401','202408')
    print(apt_price.head())
    pass