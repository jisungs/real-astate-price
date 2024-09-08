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
    

        code = pdr.code_bdong()
        df = code.loc[(code['시도명'].str.contains(sido_name)) & (code['시군구명'].str.contains(sigungu_name)) &
            (code['읍면동명']=='')]
        result = df['시군구코드'].tolist()
    
    else:
        sido_name = addr[0]
        sigungu_name = addr[1]
        code = pdr.code_bdong()
        df = code.loc[(code['시도명'].str.contains(sido_name)) & (code['시군구명'].str.contains(sigungu_name)) &
            (code['읍면동명']=='')]
        result = df['시군구코드'].tolist()

    
    if len(result) >= 2:
        return result[1]
    else:
        return result[0]
     
    
def search_apt_price(type, sigungu_code, start_year_month, end_year_month):
    # 기간 내 조회
    df = api.get_data(
        property_type=type,
        trade_type="매매",
        sigungu_code=sigungu_code,
        start_year_month=start_year_month,
        end_year_month=end_year_month,
    )
    
    return df



if __name__ == "__main__":
    sigungu_code = sigungu_code('부산', '강서구')

    print(sigungu_code)

    apt_price = search_apt_price('아파트',sigungu_code,'202401','202408')
    print(apt_price.head())
    pass