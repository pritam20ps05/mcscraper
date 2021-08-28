# MCScraper

MCScraper is a server side friendly discord bot made on python with selenium and undetected-chromedriver to ease the process of managing free aternos servers from discord guild text channels. To achieve this it uses selenium as its main driver api and to disable cloudflare detection it uses undetected-chromedriver. This bot will require to connect to your aternos account through cookies and can control all the servers to which you have proper permissions.

## Dependencies

[![](https://img.shields.io/badge/discord.py-v1.7.3-blue)](https://discordpy.readthedocs.io/en/stable/)

[![](https://img.shields.io/badge/selenium-v4.0.0b4-green)](https://selenium-python.readthedocs.io/)

[![](https://img.shields.io/badge/undetected--chromedriver-v3.0.3-pink)](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

[![](https://img.shields.io/badge/Google%20Chrome-v92.0.4515.159-yellow)](https://www.google.com/intl/en_in/chrome/)

[![](https://img.shields.io/badge/chromedriver-v92.0.4515.107-cyan)](https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.107/)

## Features

1. Server friendly
2. Modularity(multiple servers can be controlled)
3. does not have the token or cookie expiration problem like the other ones
4. it never lies

#### bot functions
$list-servers: lists all the servers that it can control

$status <server index no>: displays the current status of the mentioned status

$getinfo <server index no>: displays all the possible info about the mentioned server

$start <server index no>: starts the mentioned server 

$stop <server index no>: stops the mentioned server

![discord screenshot](https://user-images.githubusercontent.com/49360491/131210242-d85306ad-9b05-49bc-869f-3c097909eaa8.png)

## Installation / Setup

### Installing chrome and chromedriver

first we need to install the chrome for that download the package file from there [official website](https://www.google.com/chrome/?brand=YTUH&gclsrc=ds&gclsrc=ds)(Latest stable version is recomended) then install it by running the command on your terminal:

for debian or ubuntu:

```bash
sudo apt update
sudo apt install ./<filename>.deb
```
then install the chromedriver by downloading the binary from [here](https://chromedriver.chromium.org/downloads)(download the one that supports your chrome browser) after downloading copy the file and paste it in either your /usr/bin/ or /bin/ folder(for servers with different users setup /usr/bin is prefered but for running it as root user /bin/ is recomended)

### Installing pip requirements

to install all the required python packages just run the command

```bash
pip install -r requirements.txt
```

CAUTION: the charset-normalizer package can sometimes fail to install depending on your distribution and environment because its a inbuilt feature and might not be available in pip. In those cases just erase line 10 from requirements.txt file

### Creating credentials.json and servers.json

credentials.json is the file containing all of your data required to connect to your aternos account and discord bot

for that first goto the [discord developers portal](https://discord.com/developers/applications) => create an application => create a bot => copy the token of your bot

![token copy example](https://user-images.githubusercontent.com/49360491/131206823-d65cd317-a04b-4cd8-a364-e9f950e011d9.png)

then for connecting to your aternos account you need the cookies of that page. For that goto the [aternos servers page](https://aternos.org/servers/) => click on any of your servers => right click and click on inspect => goto application section and click on cookies => select https://aternos.org/ => copy and paste the cookies according to the names of them mentioned in credentials.json bellow. Don't worry if some of them are not present just leave them blank the crucial ones are ATERNOS_SESSION and PHPSESSID.

![cookie copy example](https://user-images.githubusercontent.com/49360491/131207265-75a018e5-cf29-4e7c-a44f-08d39b1aa83a.png)

#### mcscraper/credentials.json
```json
{
  "secret_key": "<Your bot token>",
  "common_cookies": {
    "one": {
      "name": "ATERNOS_SESSION",
      "value": ""
    },
    "three": {
        "name": "_ga",
        "value": ""
    },
    "four": {
        "name": "_gid",
        "value": ""
    },
    "five": {
        "name": "PHPSESSID",
        "value": ""
    },
    "six": {
        "name": "_lr_env_src_ats",
        "value": ""
    },
    "seven": {
        "name": "__gads",
        "value": ""
    },
    "eight": {
        "name": "cnx_userId",
        "value": ""
    },
    "nine": {
        "name": "_pbjs_userid_consent_data",
        "value": ""
    },
    "ten": {
        "name": "_pubcid",
        "value": ""
    },
    "eleven": {
        "name": "_pubcid_sharedid",
        "value": ""
    }
  }
}
```
to get the values in servers.json copy ATERNOS_SERVER cookie of every server you want to control and paste it accordingly with other info as shown in the snippet after the image.

![server cookie example](https://user-images.githubusercontent.com/49360491/131207754-81a62fc1-4c18-4320-923d-600c989c2da3.png)

#### mcscraper/servers.json
```json
{
  "<server name>": {
      "server_cookie": {
          "name": "ATERNOS_SERVER",
          "value": "<server cookie>"
      },
      "ip": "<server IP>",
      "port": "<server port>"
  },
  "example": {
      "server_cookie": {
          "name": "ATERNOS_SERVER",
          "value": "5dY6dRam4EXam2"
      },
      "ip": "example.aternos.me",
      "port": "45240"
  },
  ...
}
```


## Usage

there are two ways of running it first is to just directly type
```bash
python bot.py
```
which is the worst way to do it only recomended if used for testing. The best way is to create a service 

#### /lib/systemd/system/bot.service
```service
[Unit]
Description=Bot Service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
Restart=on-failure
WorkingDirectory=/<path to mcscraper folder>/mcscraper/
ExecStart=/<python interpreter bin folder>/python /<path to mcscraper folder>/mcscraper/bot.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
then run the commands

```bash
sudo systemctl daemon-reload
sudo service bot start
sudo service bot status
```
this will make the bot run even if you exit the terminal

## CAUTIONS

1. do not host it on any cloudflare blocked hosting service like heroku as the requests are flaged as bot requests
2. at least 1 core and 1 GB of RAM machine should be used or crashes might happen 

## Load Test

the test was done on a 1 core 1 GB RAM machine rather a server(ECS)

when bot is idle

![idle cpu usg](https://user-images.githubusercontent.com/49360491/131210291-e1bafd07-214f-4626-99a6-35895dde38ff.png)

when bot is under load

![load cpu usg](https://user-images.githubusercontent.com/49360491/131210340-6a7c5453-d04a-4c7f-a842-a8dc9aca130d.png)

here the cpu load is bellow 60% but expect it to get higher because in some cases it also touches 98%.

## Contributing
Feel free to contribute to it by forking or just use the code but please maintain the guidlines under the GPL 3.0 LICENSE.

## License
[GPL 3.0](https://github.com/pritam20ps05/mcscraper/blob/master/LICENSE)