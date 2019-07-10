import os
import time
# import pytest

from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


userno = os.environ.get('userno', '123456789012')

username = os.environ.get('username', 'username')
password = os.environ.get('password', 'password')

model = os.environ.get('model', 'model')


# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--single-process')
# options.add_argument('--disable-dev-shm-usage')

# browser = webdriver.Firefox()
browser = webdriver.Chrome('/usr/local/bin/chromedriver')
# browser = webdriver.Chrome(chrome_options=options)

browser.get('https://{}.signin.aws.amazon.com/console'.format(userno))

browser.find_element_by_name('username').send_keys(username)
browser.find_element_by_id('password').send_keys(password)

browser.find_element_by_id('signin_button').click()

time.sleep(5)

browser.get(
    'https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/submitModel'.format(model))

time.sleep(5)

browser.find_element_by_class_name('awsui-button-variant-primary').click()

time.sleep(5)

browser.save_screenshot('build/screenshot.png')

browser.close()
