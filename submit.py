import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from slacker import Slacker


profile = os.environ.get('PROFILE')

userno = os.environ.get('USERNO')

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

model_name = os.environ.get('MODEL', 'model')

slack_token = os.environ.get('SLACK_TOKEN', '')
slack_channal = os.environ.get('SLACK_CHANNAL', '#sandbox')


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

    browser.set_window_size(1024, 768)

    return browser


def colse_browser(browser):
    browser.close()


def login_aws(browser):
    print('login_aws')

    url = 'https://{}.signin.aws.amazon.com/console'.format(userno)

    browser.get(url)

    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)

    browser.find_element_by_id('signin_button').click()

    time.sleep(5)


def submit_model(browser):
    print('submit_model')

    url = 'https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/submitModel'.format(
        model_name)

    browser.get(url)

    time.sleep(5)

    browser.find_element_by_class_name('awsui-button-variant-primary').click()

    time.sleep(5)

    browser.save_screenshot('build/submit.png')

    # post_slack(model_name)


def result(browser):
    print('result')

    # url='https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs-insights:'
    url = 'https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs-insights:queryDetail=~(end~0~start~-3600~timeType~\'RELATIVE~unit~\'seconds~editorString~\'fields*20*40message*0a*7c*20filter*20*40message*20*3d*7e*20*27SIM_TRACE_LOG*27*20and*20*40message*20*3d*7e*20*270*2cTrue*27*0a*7c*20order*20by*20*40timestamp*20desc*2c*20*40message*20desc~isLiveTail~false~queryId~\'479f81d1-dea9-44e5-b204-867c4ca32173~source~(~\'*2faws*2fdeepracer*2fleaderboard*2fSimulationJobs))'

    browser.get(url)

    time.sleep(5)

    browser.find_element_by_id('gwt-debug-toggleButton').click()
    browser.find_element_by_class_name('side-panel-toggle-caret').click()

    browser.find_element_by_class_name('scroll-query-command-button').click()

    time.sleep(5)

    browser.save_screenshot('build/result.png')

    # post_slack(model_name)


def post_slack(text):
    print('post_slack')

    try:
        slack = Slacker(slack_token)

        # obj = slack.chat.post_message(slack_channal, text)
        # print(obj.successful, obj.__dict__['body']['channel'], obj.__dict__['body']['ts'])

        file = '{}/build/submit.png'.format(os.getcwd())
        slack.files.upload(file, channels=[slack_channal], title=text)

        # file = '{}/build/result.png'.format(os.getcwd())
        # slack.files.upload(file, channels=[slack_channal], title=text)

    except KeyError as ex:
        print('Environment variable %s not set.' % str(ex))


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

    # result(browser)

    colse_browser(browser)

    millis = int(round(time.time() * 1000))

    post_slack('%s : %s - %s' % (profile, model_name, millis))
