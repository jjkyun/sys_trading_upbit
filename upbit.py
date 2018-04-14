from selenium import webdriver
import time
import getpass
import datetime

driver = webdriver.Chrome()

upbitURL = 'https://upbit.com/exchange?code=CRIX.UPBIT.KRW-BTC'
driver.get(upbitURL)

driver.maximize_window()

time.sleep(5)
driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/header/section/span/div/a[1]').click()

time.sleep(2)
driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section/article/a').click()

time.sleep(2)

email = input('Email: ')
password = getpass.getpass('Password: ')
driver.find_element_by_xpath('//*[@id="email"]').send_keys(email)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="btn_login"]').click()
time.sleep(3)

buyTabButton = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section[1]/div/div[2]/article[1]/span[1]/ul/li[1]/a')
sellTabButton = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section[1]/div/div[2]/article[1]/span[1]/ul/li[2]/a')
amountInput = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section[1]/div/div[2]/article[1]/span[2]/div/dl/dd[2]/input')
priceInput = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section[1]/div/div[2]/article[1]/span[2]/div/dl/dd[3]/div/input')
buysellButton = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[3]/section[1]/div/div[2]/article[1]/span[2]/div/ul/li[2]/a')

def Order(order):
    if order == 'buy':
        buyTabButton.click()
    elif order == 'sell':
        sellTabButton.click()

    amountInput.clear()
    amountInput.send_keys(1)

    priceInput.clear()
    priceInput.send_keys(currentPrice)

    time.sleep(2)
    buysellButton.click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="checkVerifMethodModal"]/div/section/article/span/a').click()

while True:
    time.sleep(5)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    currentPrice = driver.title.split(' ')[0]

    Order('buy')
    time.sleep(2)
    Order('sell')
