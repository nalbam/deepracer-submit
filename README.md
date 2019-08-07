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
export SLACK_TOKEN="xoxb-1111-2222-xxxx"
export MODEL="model"
```

## usage

```bash
bash submit.sh
```

## crontab

```bash
*/12 * * * * /home/pi/deepracer-submit/submit.sh >> /home/pi/deepracer-submit.log 2>&1
```
