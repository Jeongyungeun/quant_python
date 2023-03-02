
from pandas import DataFrame
from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY, YEARLY
from collections import defaultdict
from tqdm import tqdm
from excel_process import ProcessExcel
import os
import csv
import pandas as pd
import numpy as np
from sklearn import linear_model


class Quent:
    
    def linear_regression(df:pd.DataFrame, init_quater: int)-> bool:
        df_object = df['ROE_rolling']
        df_object = df_object[-10:]
        df_object['index'] = np.arange(len(df_object.index)) + 1
    
    def roe_pbr_stock_price(self, df:DataFrame, dict: defaultdict):
        # 다시 분기별로 보기 위해
        if df is None:
            return
        try:
            value = [0, 0, 0,'']
            # 0 - roe 평균
            # 1 - 최근 PBR
            # 2 - diff
            # 3 - Name
                
            df_refix = df.drop_duplicates(subset=['매출액', '영업이익'], keep='first', inplace=False)
            # print(df_refix.iloc[-5:])
            
            # TODO ROE가 5분기 평균 10 이상 종목을 골라내자.
            df_end_five = df_refix.iloc[-5:]
            avr = df_end_five['ROE_rolling'].mean()
        
            value[0] = avr
                
            value_pbr = df_end_five.iloc[-1]['PBR']
            value[1] = value_pbr
            
            value[3] = df_end_five.iloc[-1]['Name']
            try:
                value[2] = ((value[0]/100 +1)/1.1)**3 - value_pbr
            except:
                value[2] = 0.0
            # print(value_diff)
            dict[value[3]] = value
        except:
            pass
    
        finally:
            print(value)
    
    def find_sorting_value(self, dict: dict):
        return sorted(dict.items(), reverse=True, key=lambda x : x[1][2])





# dict_example = {'sk' : [1,23,4], 'lg' : [2,3,5]}

if __name__ == '__main__':
    
    process_excel = ProcessExcel()
    quent = Quent()
    # print(quent.find_sorting_value(dict=dict_example))
    sorting = defaultdict(list)
    
    file_list = os.listdir('D:/bs_data_22')
    for file in tqdm(file_list[1000:]):
        quent.roe_pbr_stock_price(process_excel.pre_process(file), sorting)
        
    result_list = quent.find_sorting_value(sorting)
    
    

    with open('D:/sorting_result.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result_list)

    
    # quent.roe_pbr_stock_price()
    
    