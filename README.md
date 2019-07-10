# deepracer-submit

## install

```bash
sudo apt install xvfb
sudo apt install chromium-browser chromium-codecs-ffmpeg
sudo apt install chromium-chromedriver

pip3 install pytest
pip3 install selenium
pip3 install xvfbwrapper
```

## config

```bash
# config/deepracer-model.sh
export userno="123456789012"
export username="username"
export password="password"
export model="model"
```

## usage

```bash
bash submit.sh
```

## crontab

```bash
*/10 * * * * /home/pi/deepracer-submit/submit.sh >> /home/pi/deepracer-submit.log 2>&1
```
