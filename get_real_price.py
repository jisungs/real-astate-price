

from PublicDataReader import TransactionPrice
import PublicDataReader as pdr
import pandas as pd

service_key = "API_KEY"

api = TransactionPrice(service_key)

#시군구 코드 조회

def sigungu_code(sido_name, sigungu_name):
    code = pdr.code_bdong()
    df = code.loc[(code['시도명'].str.contains(sido_name)) & (code['시군구명'].str.contains(sigungu_name)) &
         (code['읍면동명']=='')]
    result = df['시군구코드']
    print(result)
    if len(result) >= 2:
       result.iloc[1]
    else:
        result.iloc[0]
    
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


sigungu_code = sigungu_code('부산', '해운대구')
print(sigungu_code)

# apt_price = search_apt_price('아파트',sigungu_code,'202401','202408')
# print(apt_price.head())
