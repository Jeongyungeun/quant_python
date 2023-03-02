import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta
import re
from marcap import marcap_data
from matplotlib import pyplot as plt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_colwidth', 100)
import os
import matplotlib.pyplot as plt
import numpy as np




class ProcessExcel:
    
    def type_check_in_column(self, column_name: str, df):
        for index in range(len(df[column_name])):
            type_info = type(df[column_name].iloc[index])
            # print(type_info)
            if type_info is str:
                data = df[column_name].iloc[index]
                if ',' in data:
                    data = data.replace(',', '')
                    # print(data)
                df[column_name].iloc[index] = int(data)
        # print(df[column_name])
                     
   
    def pre_process(self, file_name: str):
        code = file_name[:6]
        file_path = "D:/bs_data_22/{}".format(file_name)
        # name = stock.get_market_ticker_name(code)
        df = pd.read_excel(file_path)
        
        if len(df.index)<6:
            return None
        
        df['결산월'].replace('\([^)]*\)', '', regex=True, inplace=True)
        df.columns = df.columns.str.replace('\([^)]*\)', '', regex=True)
        ## df.columns = df.columns.str.replace('(원)','')
        df_marcap = marcap_data('2001-05-02', '2023-02-15', code=code)
        # print(df_marcap.columns)
        
        df.drop(['주가'], axis=1, inplace=True)
        df['결산월'] = '20' + df['결산월']
        df['결산월'] = df['결산월'].apply(lambda x: x + ' 31일' if '3월' in x or '12월' in x else x + ' 30일')
        df['결산월'].replace('년 ', '/', inplace=True, regex=True)
        df['결산월'].replace('월 ', '/', inplace=True, regex=True)
        df['결산월'].replace('일', '', inplace=True, regex=True)
        df['순이익'].replace('', 0, inplace=True, regex=True)
        df['영업이익'].replace('^[-]+$', 0, regex=True)
        df['결산월'] = pd.to_datetime(pd.to_datetime(df['결산월']), format="%Y/%m/%d")
        df = df.iloc[::-1].reset_index(drop=True)
        df = df.replace('^[-]+$', 0, regex=True)
        df = df.replace('\'', '')
        df = df.replace(',', '')
                
        self.type_check_in_column('EPS', df)
        self.type_check_in_column('자기자본', df)
        self.type_check_in_column('매출액', df)
        self.type_check_in_column('영업이익', df)
        self.type_check_in_column('순이익', df)
        self.type_check_in_column('BPS', df)
        
        # print(df)
        
        # print(df_col_t_dtype['자기자본'])
        # print(df['EPS'])
        # if(df_col_t_dtype['자기자본'] == 'object'):
        #     df['자기자본'] = df['자기자본'].str.replace(',', '').astype('int64')
        # else:
        #     pass
        # if (df_col_t_dtype['매출액'] == 'object'):
        #     df['매출액'] = df['매출액'].str.replace(',', '').astype('int64')
        # else:
        #     pass
        # # print(df['영업이익'])
        # if (df_col_t_dtype['영업이익'] == 'object'):
        #     df['영업이익'] = df['영업이익'].str.replace(',', '').astype('int64')
        #     # print(df['영업이익'])
        # else:
        #     pass
        # if (df_col_t_dtype['순이익'] == 'object'):
        #     df['순이익'] = df['순이익'].str.replace(',', '').astype('int64')
        # else:
        #     pass
        # if (df_col_t_dtype['BPS'] == 'object'):
        #     df['BPS'] = df['BPS'].str.replace(',', '').astype('int64')
        # else:
        #     pass
        
                
        # try:
        #     # print(df['EPS'])
        #     if (df_col_t_dtype['EPS'] == 'object'):
                
        #         # df['EPS'] = df['EPS'].str.replace(',', '')
        #         print('-----')
        #         # df['EPS'] = df['EPS'].astype('float')                
        #     elif (df_col_t_dtype['EPS'] == 'int64'):
                
        #         pass
        #     else:
        #         pass
        # except:
        #     pass
                
        # df['EPS'] = df['EPS'].str.replace(',', '').astype('int64')

        # print(df['자기자본'])
        # print(df.dtypes)
        df.set_index('결산월', inplace=True)
        # df['EPS'] = df['EPS'].astype('float')
        # df['영업이익'] = pd.to_numeric(df['영업이익'])
        df.loc[:, 'op_rolling'] = df.loc[:, '영업이익'].rolling(window=4).sum()
        df.loc[:, 'op_rolling'] = df.loc[:, 'op_rolling'].fillna(method='bfill')

        df.loc[:, 'earn_rolling'] = df.loc[:, '순이익'].rolling(window=4).sum()
        df.loc[:, 'earn_rolling'] = df.loc[:, 'earn_rolling'].fillna(method='bfill')

        df.loc[:, 'sale_rolling'] = df.loc[:, '매출액'].rolling(window=4).sum()
        df.loc[:, 'sale_rolling'] = df.loc[:, 'sale_rolling'].fillna(method='bfill')
        
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS'].rolling(window=4).sum()
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS_rolling'].fillna(method='bfill')

        df.loc[:, 'ROE_rolling'] = df.loc[:, 'earn_rolling'] / df.loc[:, '자기자본'] * 100
        # print(df.loc[:, 'ROE_rolling'])
        
        
        
        # df.to_csv('D:/bs_process/example.csv', mode='w')

        df_result = pd.concat([df, df_marcap], axis=1)
        df_result.loc[:,:] = df_result.loc[:,:].fillna(method='ffill')
        df_result.dropna(subset=['매출액'], inplace=True)
        df_result = df_result[['Close', '매출액', '영업이익', 'ROE_rolling', '영업이익률', '영업이익증가율', '순이익', '자기자본', 'EPS', 'ROE', 'BPS',
       'PER', 'PBR', 'PSR', 'EV/EBITDA', 'EV', 'EBITDA', '부채비율', '배당수익률',
       '주당배당금', '실제배당금', 'SPS', 'CFPS', '유보율', '영업CF', '투자CF', '재무CF', '순현금',
       'op_rolling', 'earn_rolling', 'sale_rolling', 'EPS_rolling',
       'Code', 'Name', 'Market', 'Dept', 'ChangeCode',
       'Changes', 'ChagesRatio', 'Open', 'High', 'Low', 'Volume', 'Amount',
       'Marcap', 'Stocks', 'MarketId', 'Rank']]
        
        # print(df_result.index)

        return df_result
    
    def price_sales_earning_graph(self, file_name:str):
        code = file_name[:6]
        file_path = "D:/bs_data_22/{}".format(file_name)
        # name = stock.get_market_ticker_name(code)
        df = pd.read_excel(file_path)
        
        if len(df.index)<6:
            return None
        
        df['결산월'].replace('\([^)]*\)', '', regex=True, inplace=True)
        df.columns = df.columns.str.replace('\([^)]*\)', '', regex=True)
        ## df.columns = df.columns.str.replace('(원)','')
        df_marcap = marcap_data('2001-05-02', '2023-02-15', code=code)
        # print(df_marcap.columns)
        
        df.drop(['주가'], axis=1, inplace=True)
        df['결산월'] = '20' + df['결산월']
        df['결산월'] = df['결산월'].apply(lambda x: x + ' 31일' if '3월' in x or '12월' in x else x + ' 30일')
        df['결산월'].replace('년 ', '/', inplace=True, regex=True)
        df['결산월'].replace('월 ', '/', inplace=True, regex=True)
        df['결산월'].replace('일', '', inplace=True, regex=True)
        df['순이익'].replace('', 0, inplace=True, regex=True)
        df['영업이익'].replace('^[-]+$', 0, regex=True)
        df['결산월'] = pd.to_datetime(pd.to_datetime(df['결산월']), format="%Y/%m/%d")
        df = df.iloc[::-1].reset_index(drop=True)
        df = df.replace('^[-]+$', 0, regex=True)
        df = df.replace('\'', '')
        df = df.replace(',', '')
                
        self.type_check_in_column('EPS', df)
        self.type_check_in_column('자기자본', df)
        self.type_check_in_column('매출액', df)
        self.type_check_in_column('영업이익', df)
        self.type_check_in_column('순이익', df)
        self.type_check_in_column('BPS', df)
        
        df.set_index('결산월', inplace=True)
        # df['EPS'] = df['EPS'].astype('float')
        # df['영업이익'] = pd.to_numeric(df['영업이익'])
        df.loc[:, 'op_rolling'] = df.loc[:, '영업이익'].rolling(window=4).sum()
        df.loc[:, 'op_rolling'] = df.loc[:, 'op_rolling'].fillna(method='bfill')

        df.loc[:, 'earn_rolling'] = df.loc[:, '순이익'].rolling(window=4).sum()
        df.loc[:, 'earn_rolling'] = df.loc[:, 'earn_rolling'].fillna(method='bfill')

        df.loc[:, 'sale_rolling'] = df.loc[:, '매출액'].rolling(window=4).sum()
        df.loc[:, 'sale_rolling'] = df.loc[:, 'sale_rolling'].fillna(method='bfill')
        
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS'].rolling(window=4).sum()
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS_rolling'].fillna(method='bfill')

        df.loc[:, 'ROE_rolling'] = df.loc[:, 'earn_rolling'] / df.loc[:, '자기자본'] * 100
        # print(df.loc[:, 'ROE_rolling'])

        # df.to_csv('D:/bs_process/example.csv', mode='w')

        df_result = pd.concat([df, df_marcap], axis=1)
        df_result.loc[:, 'Close'] = df_result.loc[:, 'Close'].fillna(method='ffill')
        
        # df_result['sale_rolling'].fillna(0)
        bar_width = 0.3
        # print(df.index)
        # df_remove_dupl = df.drop_duplicates(subset=['매출액', '영업이익'], keep='first', inplace=False)
        # 1. 기본 스타일 설정
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (30, 10)
        x = df_result.index.to_list()
        print(x)
        x_1 = df.index.to_list()
        print(x_1)

        y1 = df_result['Close']
        y2 = df['sale_rolling']
        y3 = df['earn_rolling']
        # print(len(df_result['sale_rolling']))
        print(df_result['2021-01-01 00:00:00':'2022-09-30 00:00:00']['sale_rolling'])
        # print(df_result['2019-09-01 00:00:00':'2020-06-30 00:00:00']['Close'])
        # plt.bar(x_1, y2)
        # plt.plot(x, y1)
        fig, ax1 = plt.subplots()
        ax1.plot(x, y1, color='blue', linewidth=0.5, label='Price')
        # ax1.set_ylim(0, 18)
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Price')
        ax1.tick_params(axis='both', direction='in')

        ax2 = ax1.twinx()
        # ax3 = ax1.twinx()
        ax2.bar(x_1, y2, color='deeppink', label='Demand', width=0.3, )
        ax2.bar(x_1 + bar_width, y3, color='purple', label='Demand', width=0.3,)
        ax2.set_ylabel(r'Demand ($\times10^6$)')
        ax2.tick_params(axis='y', direction='in')



        plt.show()

    def process_data(self, file_name: str):
        code = file_name[:6]
        file_path = "D:/bs_data_22/{}".format(file_name)
        name = stock.get_market_ticker_name(code)
        
        df_result = self.pre_process(file_name)

        df_result.loc[:, 'Marcap'] = df_result.loc[:, 'Marcap'].fillna(method='ffill')
        df_result = df_result.dropna(subset=['Marcap'])
        df_result = df_result.drop(
            ['주가', '영업이익률', '영업이익증가율', 'PER', 'PBR', 'PSR', 'High', 'Low', 'EV/EBITDA', 'EV', 'EBITDA', '매출액', '영업이익',
             '순이익', 'EPS'], axis=1)

        df_result.loc[:, ['sale_rolling', 'op_rolling', '자기자본', 'earn_rolling', 'EPS_rolling', 'BPS_rolling', 'Open',
                          'Marcap']] = df_result.loc[:,
                                       ['sale_rolling', 'op_rolling', '자기자본', 'earn_rolling', 'EPS_rolling',
                                        'BPS_rolling', 'Open', 'Marcap']].fillna(method='ffill')
        df_result = df_result.dropna(subset=['sale_rolling'])

        df_process = df_result[
            ['Open', 'sale_rolling', 'op_rolling', 'earn_rolling', 'EPS_rolling', 'BPS_rolling', '자기자본', 'Marcap']]
        df_process = df_process.dropna(subset=['Open'])

        df_process['Marcap'] = df_process['Marcap'] / 100000000

        df_process['earn_rolling'] = df_process['earn_rolling'].apply(lambda x: 1 if x <= 0 else x)
        df_process['earn_PER'] = df_process['Marcap'] / df_process['earn_rolling']
        # print(df_process['earn_PER'])
        df_process['op_PER'] = df_process['Marcap'] / df_process['op_rolling']

        df_process['earn_PER'] = df_process['earn_PER'].apply(lambda x: 0 if x < 0 else x)
        df_process['op_PER'] = df_process['op_PER'].apply(lambda x: 0 if x < 0 else x)

        df_process['PBR'] = df_process['Marcap'] / df_process['자기자본']
        df_process['PBR'] = df_process['PBR'].apply(lambda x: 0 if x < 0 else x)

        pbr_9 = df_process['PBR'].quantile(0.9) / 10
        pbr_std = df_process['PBR'].std() / 10
        pbr_max = df_process['PBR'].max()
        pbr_9_semi = round(pbr_9, 2)

        per_9 = df_process['earn_PER'].quantile(0.9) / 10
        per_std = df_process['earn_PER'].std() / 10
        per_max = df_process['earn_PER'].max()
        per_9_semi = round(pbr_9, 2)
        if per_std > 10:
            per_std = 10

        name_list = []
        for i in range(1, 11):
            pbr_multi = round(i * pbr_std, 2)
            df_process['{}_PBR'.format(pbr_multi)] = df_process['자기자본'] * pbr_std * i
            name_list.append('{}_PBR'.format(pbr_multi))
        name_list.append('Marcap')

        name_per_list = []
        for i in range(1, 11):
            per_multi = round(i * per_std, 2)
            df_process['{}_PER'.format(per_multi)] = df_process['earn_rolling'] * per_std * i
            name_per_list.append('{}_PER'.format(per_multi))
        name_per_list.append('Marcap')

        # print(df_process)
        # print(per_std)
        # print(pbr_max)
        # print(pbr_std)

        # print(name_list)
        # 그리기
        df_process.plot(y=name_list, figsize=(100, 50), title='{}'.format(name), ylabel="PBR")
        plt.savefig('D:/per_band/pbr/{}_PBR.png'.format(code))

        df_process.plot(y=name_per_list, figsize=(100, 50), title='{}'.format(name), ylabel="PER")
        plt.savefig('D:/per_band/per/{}_PER.png'.format(code))


    def process_data_onefile(self, code: str, file_list: list):

        name = stock.get_market_ticker_name(code)
        # name = '대동'
        special_file=[]
        for i in file_list:
            if code in i:
                special_file.append(i)



        file_path = "D:/bs_data_22/{}".format(special_file[0])
        df = pd.read_excel(file_path)
        df['결산월'].replace('\([^)]*\)', '', regex=True, inplace=True)
        df.columns = df.columns.str.replace('\([^)]*\)', '', regex=True)
        ## df.columns = df.columns.str.replace('(원)','')
        df_marcap = marcap_data('1995-05-02', '2022-08-29', code=code)



        df['결산월'] = '20' + df['결산월']
        df['결산월'] = df['결산월'].apply(lambda x: x + ' 31일' if '3월' in x or '12월' in x else x + ' 30일')
        df['결산월'].replace('년 ', '/', inplace=True, regex=True)
        df['결산월'].replace('월 ', '/', inplace=True, regex=True)
        df['결산월'].replace('일', '', inplace=True, regex=True)
        df['결산월'].replace('일', '', inplace=True, regex=True)
        df['순이익'].replace('', 0, inplace=True, regex=True)
        df['결산월'] = pd.to_datetime(pd.to_datetime(df['결산월']), format="%Y/%m/%d")
        df = df.iloc[::-1].reset_index(drop=True)
        df = df.replace('^[-]+$', 0, regex=True)
        df = df.replace('\'', '')
        df = df.replace(',', '')
        df.fillna(value=0)


        df_col_t_dtype = df.apply(lambda x: x.dtype)

        print(df_col_t_dtype)
        # print(df['자기자본'])
        if (df_col_t_dtype['자기자본'] == 'object'):
            df['자기자본'] = df['자기자본'].str.replace(',', '').astype('int64')
        else:
            pass
        if (df_col_t_dtype['매출액'] == 'object'):
            df['매출액'] = df['매출액'].str.replace(',', '').astype('int64')
        else:
            pass
        if (df_col_t_dtype['영업이익'] == 'object'):
            df['영업이익'].replace('-', 0, inplace=True, regex=True),
            df['영업이익'].fillna(value=0)
            # print(df[df['영업이익'].isnull()])
            # print(df['영업이익'])
            df['영업이익'] = df['영업이익'].str.replace(',', '')
            df[['영업이익']] = df[['영업이익']].astype(float)
        else:
            pass
        if (df_col_t_dtype['순이익'] == 'object'):
            df['순이익'].replace('-', 0, inplace=True, regex=True),
            df['순이익'].fillna(value=0)
            # print(df[df['영업이익'].isnull()])
            # print(df['영업이익'])
            df['순이익'] = df['순이익'].str.replace(',', '')
            df[['순이익']] = df[['순이익']].astype(float)
        else:
            pass
        if (df_col_t_dtype['BPS'] == 'object'):
            df['BPS'] = df['BPS'].str.replace(',', '').astype('int64')
        else:
            pass
        # print(df['EPS'].type)
        # df['EPS'] = df['EPS'].str.replace(',', '').astype('int64')

        # print(df['자기자본'])
        print(df.dtypes)
        df.set_index('결산월', inplace=True)
        # df['EPS'] = df['EPS'].astype('float')
        # df['영업이익'] = pd.to_numeric(df['영업이익'])
        df.loc[:, 'op_rolling'] = df.loc[:, '영업이익'].rolling(window=4).sum()
        df.loc[:, 'op_rolling'] = df.loc[:, 'op_rolling'].fillna(method='bfill')
        df.loc[:, 'earn_rolling'] = df.loc[:, '순이익'].rolling(window=4).sum()
        df.loc[:, 'earn_rolling'] = df.loc[:, 'earn_rolling'].fillna(method='bfill')
        df.loc[:, 'sale_rolling'] = df.loc[:, '매출액'].rolling(window=4).sum()
        df.loc[:, 'sale_rolling'] = df.loc[:, 'sale_rolling'].fillna(method='bfill')
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS'].rolling(window=4).sum()
        df.loc[:, 'EPS_rolling'] = df.loc[:, 'EPS_rolling'].fillna(method='bfill')

        df.loc[:, 'BPS_rolling'] = df.loc[:, 'BPS'].rolling(window=4).sum()
        df.loc[:, 'BPS_rolling'] = df.loc[:, 'BPS_rolling'].fillna(method='bfill')

        df_result = pd.concat([df, df_marcap], axis=1)

        df_result.loc[:, 'Marcap'] = df_result.loc[:, 'Marcap'].fillna(method='ffill')
        df_result = df_result.dropna(subset=['Marcap'])
        df_result = df_result.drop(
            ['주가', '영업이익률', '영업이익증가율', 'PER', 'PBR', 'PSR', 'High', 'Low', 'EV/EBITDA', 'EV', 'EBITDA', '매출액', '영업이익',
             '순이익', 'EPS'], axis=1)

        df_result.loc[:, ['sale_rolling', 'op_rolling', '자기자본', 'earn_rolling', 'EPS_rolling', 'BPS_rolling', 'Open',
                          'Marcap']] = df_result.loc[:,
                                       ['sale_rolling', 'op_rolling', '자기자본', 'earn_rolling', 'EPS_rolling',
                                        'BPS_rolling', 'Open', 'Marcap']].fillna(method='ffill')
        df_result = df_result.dropna(subset=['sale_rolling'])

        df_process = df_result[
            ['Open', 'sale_rolling', 'op_rolling', 'earn_rolling', 'EPS_rolling', 'BPS_rolling', '자기자본', 'Marcap']]
        df_process = df_process.dropna(subset=['Open'])

        df_process['Marcap'] = df_process['Marcap'] / 100000000

        df_process['earn_rolling'] = df_process['earn_rolling'].apply(lambda x: 1 if x <= 0 else x)
        df_process['earn_PER'] = df_process['Marcap'] / df_process['earn_rolling']
        # print(df_process['earn_PER'])
        df_process['op_PER'] = df_process['Marcap'] / df_process['op_rolling']

        df_process['earn_PER'] = df_process['earn_PER'].apply(lambda x: 0 if x < 0 else x)
        df_process['op_PER'] = df_process['op_PER'].apply(lambda x: 0 if x < 0 else x)

        df_process['PBR'] = df_process['Marcap'] / df_process['자기자본']
        df_process['PBR'] = df_process['PBR'].apply(lambda x: 0 if x < 0 else x)

        pbr_9 = df_process['PBR'].quantile(0.9) / 10
        pbr_std = df_process['PBR'].std() / 10
        pbr_max = df_process['PBR'].max()
        pbr_min = df_process['PBR'].min()
        pbr_gap = pbr_max-pbr_min/10
        pbr_9_semi = round(pbr_9, 2)

        per_9 = df_process['earn_PER'].quantile(0.9) / 10
        per_std = df_process['earn_PER'].std() / 10
        per_max = df_process['earn_PER'].max()
        per_9_semi = round(pbr_9, 2)
        if per_std > 10:
            per_std = 10

        name_list = []
        for i in range(1, 11):
            pbr_multi = round(i * pbr_std*2, 2)
            df_process['{}_PBR'.format(pbr_multi)] = df_process['자기자본'] * pbr_std*2 * i
            name_list.append('{}_PBR'.format(pbr_multi))
        name_list.append('Marcap')

        name_per_list = []
        for i in range(1, 11):
            per_multi = round(i * per_std, 2)
            df_process['{}_PER'.format(per_multi)] = df_process['earn_rolling'] * per_std * i
            name_per_list.append('{}_PER'.format(per_multi))
        name_per_list.append('Marcap')

        # print(df_process)
        # print(per_std)
        # print(pbr_max)
        # print(pbr_std)

        # print(name_list)
        # 그리기
        df_process.plot(y=name_list, figsize=(100, 50), title='{}'.format(name), ylabel="PBR")
        plt.savefig('D:/per_band/pbr/{}_PBR.png'.format(code))

        df_process.plot(y=name_per_list, figsize=(100, 50), title='{}'.format(name), ylabel="PER")
        plt.savefig('D:/per_band/per/{}_PER.png'.format(code))


if __name__ == '__main__':
    prcess_excel = ProcessExcel()
    prcess_excel.price_sales_earning_graph('007700_22_4_4.xlsx')
    
    