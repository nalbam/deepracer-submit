import os
import time
import urllib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from slacker import Slacker


profile = os.environ.get("PROFILE")

userno = os.environ.get("USERNO")

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

model_name = os.environ.get("MODEL", "model-name")
season = os.environ.get("SEASON", "season")

slack_token = os.environ.get("SLACK_TOKEN", "")
slack_channal = os.environ.get("SLACK_CHANNAL", "#sandbox")


def open_browser():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--single-process')
    # options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(options=options)

    # browser = webdriver.Chrome('/usr/local/bin/chromedriver')
    # browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

    browser.set_window_size(1600, 1440)

    return browser


def colse_browser(browser):
    browser.close()


def login_aws(browser):
    print("login_aws", username)

    url = "https://{}.signin.aws.amazon.com/console".format(userno)

    browser.get(url)

    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)

    browser.find_element_by_id("signin_button").click()

    time.sleep(5)


def submit_model(browser):
    print("submit_model", model_name)

    # url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/submitModel".format(
    #     model_name
    # )

    arn = urllib.quote_plus("arn:aws:deepracer:us-east-1::leaderboard/virtual-season")

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#model/{}/leaderboard/{}-{}/submitModel".format(
        model_name, arn, season
    )

    browser.get(url)

    time.sleep(10)

    browser.find_element_by_class_name("awsui-button-variant-primary").click()

    time.sleep(5)

    browser.save_screenshot("build/submit-{}.png".format(profile))


def result(browser):
    print("result")

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#league"

    browser.get(url)

    time.sleep(10)

    browser.save_screenshot("build/result-{}.png".format(profile))


def post_slack(text):
    print("post_slack")

    try:
        slack = Slacker(slack_token)

        # obj = slack.chat.post_message(slack_channal, text)
        # print(obj.successful, obj.__dict__['body']['channel'], obj.__dict__['body']['ts'])

        file = "{}/build/submit-{}.png".format(os.getcwd(), profile)
        slack.files.upload(file, channels=[slack_channal], title=text)

        file = "{}/build/result-{}.png".format(os.getcwd(), profile)
        slack.files.upload(file, channels=[slack_channal], title=text)

    except KeyError as ex:
        print("Environment variable %s not set." % str(ex))


if __name__ == "__main__":
    if userno is None or userno == "":
        raise ValueError("userno")

    if username is None or username == "":
        raise ValueError("username")

    if password is None or password == "":
        raise ValueError("password")

    browser = open_browser()

    login_aws(browser)

    submit_model(browser)

    result(browser)

    colse_browser(browser)

    millis = int(round(time.time() * 1000))

    post_slack("%s : %s - %s" % (profile, model_name, millis))
