#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import time
import json
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from slacker import Slacker


def parse_args():
    p = argparse.ArgumentParser(description="deepracer submit")
    p.add_argument("-t", "--target", default="", help="target", required=True)
    p.add_argument("-m", "--model", default="", help="model")
    p.add_argument("-d", "--debug", default="False", help="debug")
    return p.parse_args()


def open_browser(args):
    if args.debug == "True":
        return None

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    # browser = webdriver.Chrome("/usr/local/bin/chromedriver")

    browser.set_window_size(1600, 1700)

    return browser


def close_browser(browser, args):
    if args.debug == "True":
        return

    try:
        browser.close()
    except Exception as ex:
        print("Error", ex)


def login_aws(doc, args, browser):
    print("+ login_aws", doc["username"])

    url = "https://{}.signin.aws.amazon.com/console".format(doc["userno"])

    if args.debug == "True":
        print("url: ", url)
        return

    # screenshot = "config/login-{}.png".format(doc["userno"])

    browser.get(url)

    time.sleep(5)

    # browser.save_screenshot(screenshot)

    browser.find_element(By.ID, "username").send_keys(doc["username"])
    browser.find_element(By.ID, "password").send_keys(doc["password"])

    browser.find_element(By.ID, "signin_button").click()

    time.sleep(5)

    # browser.save_screenshot(screenshot)


def submit_model(doc, args, browser):
    print("+ submit_model", args.target)

    arn = ""
    model = ""

    for attrs in doc["leaderboards"]:
        if attrs["name"] == args.target:
            arn = attrs["arn"]
            models = attrs["models"]

            if args.model != "":
                model = args.model
            elif len(models) > 0:
                model = random.choice(models)

            break

    if arn == "":
        print("Not found arn.")
        return

    if model == "":
        print("Empty model.")
        return

    # #league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F9f6ca6de-ecfa-467a-a7d9-c899a811a206/submitModel
    # #league/arn%3Aaws%3Adeepracer%3A%3A%3Aleaderboard%2F55234c74-2c48-466d-9e66-242ddf05e04d/submitModel
    # #competition/arn%3Aaws%3Adeepracer%3A%3A082867736673%3Aleaderboard%2Fe9fbfc93-ed99-494c-8b61-ac13a2274859/submitModel

    url = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#{}/submitModel".format(
        arn
    )

    screenshot = "config/submit-{}.png".format(args.target)

    if args.debug == "True":
        print("arn: ", arn)
        print("model: ", model)
        print("url: ", url)
        return

    try:
        browser.get(url)

        time.sleep(5)

        browser.save_screenshot(screenshot)

        browser.find_element(By.CLASS_NAME, "awsui-dropdown-trigger").click()

        path = '//*[@title="{}"]'.format(doc.model)
        browser.find_element(By.XPATH, path).click()

        browser.find_element(By.CLASS_NAME, "awsui-button-variant-primary").click()

        time.sleep(10)

        browser.save_screenshot(screenshot)
    except Exception as ex:
        print("Error", ex)

    post_slack(doc, "{} : {}".format(args.target, model), screenshot)


def post_slack(doc, text, screenshot):
    if doc["slack"]["token"] == "":
        return

    print("+ post_slack", doc["slack"]["channel"])

    filepath = "{}/{}".format(os.path.dirname(os.path.realpath(__file__)), screenshot)

    try:
        slack = Slacker(doc["slack"]["token"])

        slack.files.upload(filepath, channels=[doc["slack"]["channel"]], title=text)

    except KeyError as ex:
        print("Environment variable %s not set." % str(ex))


def main():
    args = parse_args()

    if args.target == "":
        print("Empty target.")
        return

    filepath = "{}/config/deepracer.json".format(
        os.path.dirname(os.path.realpath(__file__))
    )

    if os.path.exists(filepath):
        if args.debug == "True":
            print("filepath : {}".format(filepath))

        doc = None

        with open(filepath, "r") as file:
            doc = json.load(file)

            if doc["userno"] == "":
                print("Empty userno.")
                return

            browser = open_browser(args)

            login_aws(doc, args, browser)

            submit_model(doc, args, browser)

            close_browser(browser, args)


if __name__ == "__main__":
    main()
