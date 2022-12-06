# [Youtube Uploader Bot](https://tx.me/Utubeitbot)
[![GitHub forks](https://img.shields.io/github/forks/oVo-HxBots/Utubeitbot?&style=flat-square&logo=github)](https://github.com/oVo-HxBots/Utubeitbot/fork)
![Repo Size](https://img.shields.io/github/repo-size/oVo-HxBots/Utubeitbot?&style=flat-square&logo=github)
[![GitHub stars](https://img.shields.io/github/stars/oVo-HxBots/Utubeitbot?&style=flat-square&logo=github)](https://github.com/oVo-HxBots/Utubeitbot/stargazers)

#### [Render Support Added](#render)
#### ~~[Koyeb Support Discontinued](#koyeb)~~

> Simple [Telegram Bot](https://core.telegram.org/bots "Telegram Bots") to Upload videos to [Youtube](https://youtube.com "YouTube") written in Python3.

### Contents

- [Info](#info)
- [Libraries Used](#libraries-used)
- [Setup](#setup)
- [Heroku](#heroku)
- [Render](#render)
- [Koyeb](#koyeb)
- [Status](#status)
- [Special Notes](#special-notes)
- [Screenshots](#screenshots)
- [Video Tutorial](#video-tutorial)
- [Contact](#contact)
- [License](#license)

## How To Deploy; [See Video Here](https://youtu.be/JltFDW5X4Y0) 

### Info

This is a simple hobby project which I was really curious about to implement. This is a Telegram bot which uses [Youtube Data API v3](https://developers.google.com/youtube/v3/ "Youtube Data API v3") to upload videos to Youtube.

### Libraries Used

- [Pyrogram](https://github.com/pyrogram/pyrogram "Pyrogram")
- [Google Client API](https://github.com/googleapis/google-api-python-client "Google Client API")

### Setup

:heavy_exclamation_mark: This project requires Python3.6 or higher

**Clone and setup virtual environment**

```bash
$ git clone https://github.com/oVo-HxBots/Utubeitbot.git

$ cd Utubeitbot

$ python3 -m venv venv

$ source venv/bin/activate

```

**Environment Variables**

- `BOT_TOKEN`(Required) - Get your bot token from [Bot Father](https://tx.me/BotFather "Bot Father").
- `SESSION_NAME`(optional) - Your bot's username.
- `API_ID`(Required) - Your telegram api id, get from [Manage Apps](https://my.telegram.org).
- `API_HASH`(Required) - Your telegram api hash, get from [Manage Apps](https://my.telegram.org).
- `CLIENT_ID`(Required) - Your google client id.
- `CLIENT_SECRET`(Required) - Your google client secret.
- `BOT_OWNER`(Required) - Telegram id of bot owner.
- `AUTH_USERS`(optional) - Telegram id's of authorised users, separated by `,`.
- `VIDEO_DESCRIPTION`(optional) - Any default description to be aded to the video.
- `VIDEO_CATEGORY`(optional) - YouTube's video category id. If not specified or specified id is invalid, category id will be selected randomly.
- `VIDEO_TITLE_PREFIX`(optional) - Any prefix to be added to the video's title.
- `VIDEO_TITLE_SUFFIX`(optional) - Any suffix to be added to the video's title.
- `UPLOAD_MODE`(optional) - The video's privacy status. Valid values for this property are: `private`, `public`, `unlisted`.
- `DEBUG` (optional) - Whether to set logging level to DEBUG. If set logging will be set to DEBUG level, else INFO level.

**Getting your `CLIENT_ID` and `CLIENT_SECRET`**

- Head to [Google console](https://console.developers.google.com "Google console"), create a new project named `Youtube Uploader` and enable `API'S AND SERVISES`. Search for `YOUTUBE DATA API v3` and enable the API. Go to [Credentials](https://console.developers.google.com/apis/credentials "Credentials") page, select your project `Youtube Uploader` create a new credential with `desktop` as type. Copy the `CLIENT_ID` and `CLIENT_SECRET`.
- You have to verify your application with google, only then you can make the uploaded videos public. YouTube changed its developer policy, and videos uploaded using unverfied applications will be kept private.

**Install requirements**

Run :

```bash
$ pip3 install -r requirements.txt
```

**Run bot**

Lets run our bot for the first time!

```bash
$ python3 -m bot
```

If you did everything correctly, the bot should be running. Go do `/start` to see if the bot is live or not. Follow the instructions provided by bot to setup authorisation and to start uploading.

#### Heroku

**Or the easy way of directly deploying to heroku**

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

#### Render
<p align="center">
<img  width="25%" height="25%" src="./ss/render1.jpg">
<img  width="25%" height="25%" src="./ss/render2.jpg">

[See more on our blog with youtube video](https://hxbots.eu.org/2022/12/deploy-youtube-uploader-bot-on-render/)

**the easy way of directly deploying on render**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/oVo-HxBots/Utubeitbot)

#### Koyeb
<p align="center">
<img  width="25%" height="25%" src="./ss/koyeb1.jpg">
<img  width="25%" height="25%" src="./ss/koyeb2.jpg">

### Development Status

This project is actively maintained and will continue so until I'm tired of it.

### Special notes

- With the Youtube Data API you are awarded with 10,000 points of requests. For one video upload it costs 1605 points, regardless of file size, which calculates to about 6 uploads daily. Once you have exhausted your daily points, you have to wait till daily reset. Resets happens at 0:00 PST, i.e. 12:30 IST. So make your uploads count.

- Uploading copyright contents will leads to immediate blocking of the video.

- By default, all the videos are uploaded as private with random category id unless you provide `UPLOAD_MODE` and `VIDEO_CATEGORY`. You may change it after youtube processes the video.

### Screenshots

<p align="center">

<img  width="25%" height="25%" src="./ss/overview.jpg">

<img  width="25%" height="25%" src="./ss/bot-start.jpg">

<img  width="25%" height="25%" src="./ss/bot-help.jpg">

<img  width="25%" height="25%" src="./ss/bot-authorise.jpg">

<img  width="25%" height="25%" alt="Upload" src="./ss/bot-upload.jpg">

</p>

### Video Tutorial

Here's a YouTube tutorial video for deploying the bot on [Heroku](https://heroku.com/ "Heroku"). [Video Link](http://www.youtube.com/watch?v=LSs8b5dMWIA "Tutorial video for deploying to Heroku").

### Contact

You can contact me [@hxSupport](https://telegram.dog/hxSupport "hxSupport").

### License

Code released under [GNU General Public License v3.0](LICENSE).
