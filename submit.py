#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import time
import json
import random
import pyotp

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


BASE_URL = "https://us-east-1.console.aws.amazon.com/deepracer/home?region=us-east-1"


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
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    )

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

    # url = "https://{}.signin.aws.amazon.com/console".format(doc["userno"])
    url = "https://console.aws.amazon.com/console/home?region=us-east-1"

    if args.debug == "True":
        print("url: ", url)
        return

    message = "login {} - {}".format(args.target, doc["username"])
    screenshot = "{}/config/login-{}.png".format(realpath(), args.target)

    try:
        browser.get(url)

        time.sleep(5)

        browser.find_element(By.ID, "aws-signin-general-user-selection-iam").click()
        browser.find_element(By.ID, "iam_user_radio_button").click()

        browser.find_element(By.ID, "resolving_input").send_keys(doc["userno"])

        if doc["debug"] == "True":
            browser.save_screenshot(screenshot)
            post_slack(doc, message, screenshot)

        browser.find_element(By.ID, "next_button").click()

        time.sleep(5)

        # browser.find_element(By.ID, "account").send_keys(doc["userno"])

        browser.find_element(By.ID, "username").send_keys(doc["username"])
        browser.find_element(By.ID, "password").send_keys(doc["password"])

        if doc["debug"] == "True":
            browser.save_screenshot(screenshot)
            post_slack(doc, message, screenshot)

        browser.find_element(By.ID, "input_signin_button").click()

        time.sleep(5)

        if doc["mfa"] != "" and doc["mfa"] != "NONE":
            totp = pyotp.TOTP(doc["mfa"])

            browser.find_element(By.ID, "mfacode").send_keys(totp.now())

            if doc["debug"] == "True":
                browser.save_screenshot(screenshot)
                post_slack(doc, message, screenshot)

            browser.find_element(By.ID, "submitMfa_button").click()

            time.sleep(5)

    except Exception as ex:
        print("Error", ex)

    if doc["debug"] == "True":
        browser.save_screenshot(screenshot)
        post_slack(doc, message, screenshot)


def submit_model(doc, args, browser):
    print("+ submit_model", args.target)

    arn = ""
    model = ""

    for attrs in doc["races"]:
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

    url = "{}#{}/submitModel".format(BASE_URL, arn)

    if args.debug == "True":
        print("arn: ", arn)
        print("model: ", model)
        print("url: ", url)
        return

    message = "submit {} - {}".format(args.target, model)
    screenshot = "{}/config/submit-{}.png".format(realpath(), args.target)

    post_slack(doc, message)

    try:
        browser.get(url)

        time.sleep(5)

        print("click", "//body")
        click_element_xpath(browser, "//body")

        # # dismiss popup
        # click_element_css(browser, "button[class^='awsui_dismiss-button']")

        time.sleep(1)

        # show models
        print("click", "show models")
        # awsui_button-trigger_18eso_1wwwd_103 awsui_has-caret_18eso_1wwwd_170
        click_element_css(browser, "button.awsui_has-caret_18eso_1wwwd_170")

        time.sleep(1)

        # select model
        print("click", "select model")
        click_element_xpath(browser, '//*[@title="{}"]'.format(model), "../..")

        time.sleep(1)

        # submit
        print("click", "submit")
        # awsui_button_vjswe_2od9j_107 awsui_variant-primary_vjswe_2od9j_251
        click_element_css(browser, "button[class*='awsui_variant-primary']")

        time.sleep(10)

    except Exception as ex:
        print("Error", ex)

    browser.save_screenshot(screenshot)
    post_slack(doc, message, screenshot)


def click_element_xpath(browser, selector, parent=None):
    try:
        e = browser.find_element(By.XPATH, selector)
        # print("elements", e.size if e is not None else 0)
        if parent is None:
            e.click()
        else:
            e.find_element(By.XPATH, parent).click()
    except Exception as ex:
        print("Error", ex)


def click_element_css(browser, selector, parent=None):
    try:
        e = browser.find_element(By.CSS_SELECTOR, selector)
        # print("elements", e.size if e is not None else 0)
        if parent is None:
            e.click()
        else:
            e.find_element(By.XPATH, parent).click()
    except Exception as ex:
        print("Error", ex)


def insert_element_css(browser, selector, value):
    try:
        browser.find_element(By.CSS_SELECTOR, selector).send_keys(value)
    except Exception as ex:
        print("Error", ex)


def post_slack(doc, text, screenshot=""):
    if doc["slack"]["token"] == "":
        return

    token = doc["slack"]["token"]
    channel = doc["slack"]["channel"]

    print("+ post_slack", channel)

    client = WebClient(token)

    try:
        if screenshot == "":
            client.chat_postMessage(channel=channel, text=text)
        else:
            client.files_upload(channels=channel, file=screenshot, title=text)
    except SlackApiError as e:
        print("Error", e.response["error"])


def realpath():
    return os.path.dirname(os.path.realpath(__file__))


def main():
    args = parse_args()

    if args.target == "":
        print("Empty target.")
        return

    filepath = "{}/config/deepracer.json".format(realpath())

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
