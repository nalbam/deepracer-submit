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
export USERNO="123456789012"
export USERNAME="username"
export PASSWORD="password"
export MODEL="model"
export SLACK_TOKEN=""
```

## usage

```bash
bash submit.sh
```

## crontab

```bash
*/5 * * * * /home/pi/deepracer-submit/submit.sh >> /home/pi/deepracer-submit.log 2>&1
```
