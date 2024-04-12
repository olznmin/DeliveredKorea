# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 
from selenium.webdriver.common.by import By
import json
# 크롬 드라이버 자동 업데이트을 위한 모듈
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import json 
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import locale

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# 불필요한 에러 메시지 삭제
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 최신 버전 설정
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)

#숫자 천단위 쪼개는 모듈 
locale.setlocale(locale.LC_ALL,'')

#우회용 delay 
time.sleep(random.uniform(1,3))
# 웹페이지 해당 주소 이동
browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

# 자동방지 우회 로그인 
input_js = ' \
        document.getElementById("id").value = "{id}"; \
        document.getElementById("pw").value = "{pw}"; \
    '.format(id = "dkjayden", pw = "a796796796")
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.execute_script(input_js)
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.find_element(By.ID,"log.login").click()

# 터미널에서 URL 입력 받기
# url = input("웹 페이지 URL을 입력하세요: ")

#Json 파일 불러오는 코드 
filename = input("구매하고 싶은 파일명을 입력하세요 : ")
with open(filename+'.json','r',encoding='utf-8')as f:
    data = json.load(f)

#url 저장 
url = data[0].get('Product_URL')
if data is not None and isinstance(data, list) and len(data) > 0 and 'option' in data[0] and isinstance(data[0]['option'], list) and len(data[0]['option']) > 0 and 'price' in data[0]['option'][0]:
    option_price = data[0]['option'][0]['price']

if data is not None and isinstance(data, list) and len(data) > 0 and 'optionCombinations' in data[0] and isinstance(data[0]['optionCombinations'], list) and len(data[0]['optionCombinations']) > 0 and 'price' in data[0]['optionCombinations'][0]:
    combination_price = data[0]['optionCombinations'][0]['price']

# 웹페이지 해당 주소 이동
browser.get(url)

# 변수, 리스트, 객체 모음
# 'optionName'의 값을 'optionname'에 저장
optionnames = {}
option = data[0].get('option') if len(data) > 0 else None
if not isinstance(option, list):
    option = [{}]
        
if option and option[0]:
    for i in range(1, 11):
        key = 'optionName' + str(i)
        if key in option[0]:
            optionnames[key] = option[0][key]
# optionCombinations 의 값을 'name'에 저장  
name_values, name_values1, name_values2 = [], [], []
name, price, price1 = [], [], []

optionCombinations = data[0].get('optionCombinations') if len(data) > 0 else None

if not isinstance(optionCombinations, list):
    optionCombinations = [{}]

for option in optionCombinations:
    if 'price' in option:
        price.append(" ("+ str(option['price']) +"원)")
        price1.append(" (+"+ str(option['price'])+"원)")

    if 'name' in option:
        name.append(option['name'])

#장바구니 xpath
xpath_list=[
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/div[2]/div[3]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[9]/div[2]/div[3]/a',
'//*[@id="content"]/div[3]/div[2]/fieldset/div[9]/div[2]/div[3]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/div[2]/div[2]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[7]/div[2]/div[3]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[11]/div[2]/div[3]/a',
'//*[@id="content"]/div[2]/div[2]/fieldset/div[11]/div[2]/div[3]/a',
'//*[@id="content"]/div[3]/div[2]/fieldset/div[10]/div[2]/div[3]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[10]/div[2]/div[3]/a',
'//*[@id="content"]/div/div[2]/div[2]/fieldset/div[9]/div[2]/div[3]/a'
]

#주문하기 xpath
order_xpath_list=[
        '//*[@id="app"]/div/div[9]/div/div[2]/button[2]',
        '//*[@id="app"]/div/div[10]/div/div[2]/button[2]'
]

#단일 상품 확인코드 
def start():
    if optionnames.get('optionName1') == None :
        count = input('주문하고싶은 상품의 수량을 입력하세요')
            
        element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.bd_EZ05h.bd_2nJMW.N\\=a\\:pcs\\.quantity')))

        if element is not None:
            element_text = browser.find_element(By.CSS_SELECTOR, '.bd_2eiJL.N\\=a\\:pcs\\.quantity').text
            value = 0  # value를 0으로 초기화합니다.
            if element_text:
                value = int(element_text)
            else:
                print("단일 상품의 제품을 선택합니다.")

        count = int(count)
        while value < count:
            element.click()
            value = int(browser.find_element(By.CSS_SELECTOR, '.bd_2eiJL.N\\=a\\:pcs\\.quantity').get_attribute('value'))  
            print ('상품 개수를 맞게 선택하였습니다.')
    else:
        for i, (option_key, option_value) in enumerate(optionnames.items(), start=1):
            if option_key.startswith("optionName"):
                option_product(i-1, option_value)


#옵션상품 코드
def option_product(option_index, option_name):
    elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bd_1fhc9.N\\=a\\:pcs\\.opopen')))
    
    element = elements[option_index]
    element.click()

    price_option = f"{option_name} ({option_price}원)"
    plusprice_option = f"{option_name} (+{option_price}원)" 

    ul_element = browser.find_element(By.CLASS_NAME, 'bd_zxkRR')
    tags = ul_element.find_elements(By.XPATH, './li')

    for tag in tags:
        if tag.text == option_name:
            tag.click()
            break
        elif tag.text == price_option:
            tag.click()
            break
        elif tag.text == plusprice_option:
            tag.click()
            break

#추가상품 코드
def combination():
    elements = WebDriverWait(browser, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.bd_2gVQ5')))

    formatted_price = []
    formatted_price2 = []

    for i in price:
        nums = re.findall(r'\d+',i)
        formatprice = i
        for num in nums:
            formatted_num = locale.format_string("%d",int(num),grouping=True)
            formatprice = formatprice.replace(num, formatted_num)
            formatted_price.append(formatprice)

    for i in price1:
        nums = re.findall(r'\d+',i)
        formatprice2 = i
        for num in nums:
            formatted_num = locale.format_string("%d",int(num),grouping=True)
            formatprice2 = formatprice2.replace(num, formatted_num)
            formatted_price2.append(formatprice2)

    product_list = []
        
    for i in range(0, len(formatted_price)):
        product_list.append(name[i]+formatted_price[i])
        product_list.append(name[i]+formatted_price2[i])

    for element in elements:
        try:
            element.click()
            ul_element = browser.find_element(By.CLASS_NAME, 'bd_23biA')
            tags = ul_element.find_elements(By.XPATH, './li')
            for tag in tags:
                if tag.text in product_list:
                    tag.click()
        except:
            continue

# 장바구니 버튼 클릭 
def shopping_basket(xpath):
    try:
        element = WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH,xpath)))
        element.click()
        element.send_keys(Keys.RETURN)
        print("장바구니버튼 웹 요소를 성공적으로 클릭하고 엔터키를 눌렀습니다.")
        return True
    except TimeoutException:
        return False

#장바구니창 alert 진입 코드
def alert(): 
    time.sleep(1)
    try:
        alert = browser.switch_to.alert  # alert 창으로 포커스를 전환합니다.
        alert.accept()  # alert 창의 확인 버튼을 누릅니다.
    except:
        print("No alert present.")

# 주문하기 
def order(xpath):
        try:
            element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.XPATH,xpath)))
            element.click()
            element.send_keys(Keys.RETURN)
            print("총 주문하기 버튼을 눌렀습니다. ")
            return True 
        except:
            return False
        
# Main Code  
try:
    # 도착보장 상품 예외처리 
    element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'._1SHgFqYghw._1NXyF7xfLC')))
    print ('ERROR: 도착보장 상품은 구매할 수 없습니다.')
    browser.close()
except:
    try:
        #단일 상품 혹은 기본 옵션 선택 함수
        start()
        # 추가옵션 선택 함수
        try:
            combination()
            #장바구니 클릭 버튼 실행 함수 
            for xpath in xpath_list:
                if shopping_basket(xpath):
                    break
            else:
                print("장바구니 버튼을 찾는데 실패했습니다.")
            # 장바구니 버튼 실행시 나오는 alert 처리 함수 
            alert()
            # 주문하기 함수 
            for xpath in order_xpath_list:
                if order(xpath):
                    break
                else:
                    print("총 주문하기 버튼을 찾는데 실패했습니다.")
        except:
            #장바구니 클릭 버튼 실행 함수 
            for xpath in xpath_list:
                if shopping_basket(xpath):
                    break
            else:
                print("장바구니 버튼을 찾는데 실패했습니다.")
            # 장바구니 버튼 실행시 나오는 alert 처리 함수 
            alert()
            # 주문하기 함수 
            for xpath in order_xpath_list:
                if order(xpath):
                    break
                else:
                    print("총 주문하기 버튼을 찾는데 실패했습니다.")
    except:
        print("Error: 오류 발생")