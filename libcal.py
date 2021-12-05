from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from timeit import default_timer as timer
from datetime import datetime
import warnings
import pause
import time
import os

def uvt_sso(browser, wait):

    browser.get('https://tilburguniversity.libcal.com/r')

    #reserve
    rb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="s-lc-new-reservation-start"]')))
    rb.click()

    #username, password, login 
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys(a)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(b)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@name="login"]'))).click()

if __name__ == '__main__':

    os.environ['WDM_LOG_LEVEL'] = '0'
    warnings.filterwarnings("ignore", category=DeprecationWarning) 

    a = ''
    b = ''
    start_time = '10:00pm'
    end_time = '11:15pm'
    day = 9
    date = '{}/12/2021'.format(day)
    seat = 'Floor 2 North, L 1'
    seat_url = 'https://tilburguniversity.libcal.com/seat/141205'



    print('--------------------------------')
    print('USERNAME: {}'.format(a))
    print('SEAT: {}'.format(seat))
    print('DATE: {}'.format(date))
    print('START_TIME: {}'.format(start_time))
    print('END_TIME: {}'.format(end_time))
    print('--------------------------------')

    browser = webdriver.Chrome(ChromeDriverManager(
        chrome_type=ChromeType.CHROMIUM).install())
    wait = WebDriverWait(browser, 12)
    uvt_sso(browser, wait)

    browser.get(seat_url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="eq-time-grid"]/div[1]/div[1]/button[1]'))).click()

    #yyyy, #mm, #d, #h, #m
    pause.until(datetime(2021, 12, 5, 12, 14))
    wait.until(EC.presence_of_element_located((By.XPATH, '//td[@class="day" and contains(text(), "{}")]'.format(day)))).click()

    start = timer()

    timeblock = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@title, "{}")]'.format(start_time))))
    slider = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="eq-time-grid"]/div[2]/div/table/tfoot/tr/td[3]/div/div')))

    while True:
        try:

            timeblock.click()
            end = timer()
            print('timer: {}'.format(end-start))
            break

        except Exception as e:

            slider.click()
    
    options = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//option[@data-crc]')))

    for el in options:
        if end_time in el.text:
            val = el.get_attribute('value')

    until = Select(wait.until(EC.presence_of_element_located((By.XPATH, '//select[contains(@id, "bookingend")]'))))
    until.select_by_value(val)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="submit_times"]'))).click()

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q1045"]'))).send_keys(a[1:])
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="s-lc-eq-bform"]/fieldset/div[5]/fieldset/div/div/div/label/input'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="s-lc-eq-bform-submit"]'))).click()

    time.sleep(2000)
