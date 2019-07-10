# deepracer-submit

## raspberrypi

* 2018-11-13-raspbian-stretch

## usage

```bash
pip3 install pytest
pip3 install selenium

export userno="123456789012"
export username="username"
export password="password"
export model="model"

pytest submit.py
```

## chromium

```bash
sudo apt install chromium-browser chromium-codecs-ffmpeg
sudo apt install chromium-chromedriver

dpkg -l | grep chromium
```
