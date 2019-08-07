# deepracer-submit

## install

```bash
sudo apt install xvfb
sudo apt install chromium-browser chromium-codecs-ffmpeg
sudo apt install chromium-chromedriver

pip3 install pytest
pip3 install selenium
pip3 install xvfbwrapper
pip3 install slacker
```

## config

```bash
# config/deepracer-model.sh
export PROFILE_URL=""
export MODEL_URL=""

export USERNO="123456789012"

export USERNAME="username"
export PASSWORD="password"

export MODEL="model"

export SLACK_TOKEN="xoxb-1111-2222-xxxx"
```

## usage

```bash
bash submit.sh
```

## crontab

```bash
0,12,24,36,48 * * * * /home/pi/deepracer-submit/submit.sh > /tmp/deepracer-submit.log 2>&1
```
