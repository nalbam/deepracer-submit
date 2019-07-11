import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


userno = os.environ.get('userno')

username = os.environ.get('username')
password = os.environ.get('password')

model = os.environ.get('model', 'model')


def open_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--single-process')
    # options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)

    # browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    # browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    return browser


def colse_browser(browser):
    browser.close()


def login_aws(browser):
    browser.get('https://{}.signin.aws.amazon.com/console'.format(userno))

    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)

    browser.find_element_by_id('signin_button').click()

    time.sleep(5)


def submit_model(browser):
    browser.get(
        'https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/submitModel'.format(model))

    time.sleep(5)

    browser.find_element_by_class_name('awsui-button-variant-primary').click()

    time.sleep(5)

    browser.save_screenshot('build/screenshot.png')


if __name__ == '__main__':
    if userno is None or userno == '':
        raise ValueError('userno')

    if username is None or username == '':
        raise ValueError('username')

    if password is None or password == '':
        raise ValueError('password')

    browser = open_browser()

    login_aws(browser)

    submit_model(browser)

    colse_browser(browser)
