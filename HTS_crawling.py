import pyautogui
import time
from datetime import datetime


def hts_to_excel(code_list, name_list):
    #
    # pyautogui.countdown(3)
    #
    # pyautogui.moveTo(539, 1051, duration=0.1)
    # pyautogui.click()
    # time.sleep(1)
    #
    # # pyautogui.moveTo(804, 720, duration=0.1)
    #
    #
    # time.sleep(19)
    # pyautogui.write(['!', 'w', 'j', 'd', 'd', 'b', 's', 'r', 'm', 's', '3', '@'], interval=0.5)
    # pyautogui.press('ENTER')
    # time.sleep(20)
    # print("공인인증서")
    #
    # pyautogui.moveTo(100, 94, duration=1)
    # # Point(x=114, y=128)
    # pyautogui.click()
    # time.sleep(2)
    #
    # pyautogui.write(['0', '6', '0', '1'], interval=0.5)
    # time.sleep(2)
    # print("재무추이 선택")

    pyautogui.countdown(5)

    # 코드 적기
    date_today = '22_4_4'
    # 데이터 저장 분기
    code_num = 0
    for code, name_ in zip(code_list, name_list):
        code_num += 1
        print(code_num)
        pyautogui.click(91, 193)
        # Point(x=114, y=243)
        pyautogui.write(code, interval=0.1)

        # 스크롤하기
        pyautogui.moveTo(1910, 924, duration=1)
        time.sleep(3)
        pyautogui.click(duration=0.1)
        time.sleep(3)
        pyautogui.click(duration=0.1)
        time.sleep(3)
        pyautogui.click(duration=0.1)
        # 엑셀 클릭해서 저장
        pyautogui.moveTo(1178, 324, duration=1)
        pyautogui.click(button='RIGHT')

        # 엑셀로 내보내기
        pyautogui.moveTo(1285, 853, duration=2)
        pyautogui.click()
        time.sleep(6)
        # 엑셀 클릭
        pyautogui.moveTo(286, 1049, duration=1)
        pyautogui.click()

        time.sleep(3)

        filename = code + '_' + date_today


# 한글을 오토핫키로 적는 법.
    # def my_write(text):
    #     pyperclip.copy(text)
    #     pyautogui.hotkey("ctrl", "v")





        # 저장하기
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)
        pyautogui.write(filename, interval=0.5)
        # pyautogui.write(my_write(name_), interval=0.3)
        pyautogui.press('ENTER')
        time.sleep(2)
        pyautogui.hotkey('altleft', 'f4')
        time.sleep(4)

    # with open(r"E:\2021_year\Stock\python_bs\{}.txt".format(date_today+"filename_list"), 'w') as f:
    #     f.write(filename_list)
    #
    #
    # return filename_list

if __name__=="__main__":
    time.sleep(3)
    print(pyautogui.position())






# 데이터 베이스로 저장하기
# data = pd.read_excel(r'E:\2021_year\Stock\python_bs\{}.xlsx'.format(filename))
# data_1 = data[::-1]
#
# 칼럼명 수정
# col_list = ['settle_mon', 'price', 'sale', 'op', 'op_rate', 'op_gr', 'np', 'equity', 'eps', 'bps', 'per', 'pbr', 'roe', 'psr', 'ev_ebitda', 'ev', 'ebitda', 'debt_r', 'divi_r', 'divi_per_shar', 'actu_divi', 'sps', 'cfps', 'rserv_r', 'oper_cf', 'invst_cf', 'finan_cf', 'net_cash']








# pyautogui.moveTo(101, 112, duration=1)
# pyautogui.doubleClick(interval=0.1)
# for i in pyautogui.getAllWindows():
#     print(i.title) #창의 재목정보
# pyautogui.write('0601')
# # time.sleep(9)
#
# pyautogui.moveTo(847,861,duration=1)
# time.sleep(7)
#
# pyautogui.click(duration=0.1)
# login = pyautogui.locateOnScreen("login.png")
#
# pyautogui.moveTo(login)
#
# pyautogui.click(duration=0.1)
#
# time.sleep(5)



# pyautogui.write('!wjddbsrms3@', interval=0.2)


#
# time.sleep(2)
# pyautogui.moveTo(1407,1022, duration=0.1)
#
# pyautogui.click()
# pyautogui.write('!wjddbsrms3@')


# pyautogui.mouseDown()
# pyautogui.mouseUp()
# time.sleep(3)

# time.sleep(2)
# pyautogui.press("ENTER")
#
