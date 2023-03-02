# PS D:\python_data> git clone "https://github.com/FinanceData/marcap.git" marcap
# marcap 데이터 얻기
from HTS_crawling import hts_to_excel
from excel_process import Process_excel
from ticker import Ticker
import os


if __name__ == '__main__':

####################################################################################
    ticker_instant = Ticker()
    ticker_list = ticker_instant.get_tiker()
    ticker_name = ticker_instant.name_from_ticker(ticker_list=ticker_list)
    # print(ticker_name[-1])

    # hts 로부터 excel 얻기
    ticker_num_adjust = ticker_list[1000:]
    name_num_adjust = ticker_name[1000:]
    # print(ticker_num_adjust)
    hts_to_excel(code_list=ticker_num_adjust, name_list=name_num_adjust)

#################################################################################520_2


    # file_list = os.listdir('D:/bs_data_22')
    # process_excel = Process_excel()
    # # for i in file_list:
    # #     prcess_excel.process_data(file_name=i)
    # process_excel.process_data_onefile('000490', file_list)


#################################################################################

