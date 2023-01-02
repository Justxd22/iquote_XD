# iquote_XD


Code for the instagram bot [@xd_quote](https://instagram/xd_quote/)

Features :] :
 - Generate HD images in instant
 - Random quotes on every run
 - 1 post every 5hrs
 - Uses gquote library made by ME!
 - Very low hardware usage you can run it in the background
 - Error reporting to telegram

enjoy :)


# Setup
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/h?referralCode=4_MSke)
[![Deploy on Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Justxd22/Emotions_XD)

### Requirements
  - Redis db  
    needed for storing last time posted, to keep the post every 5hrs cycle
  - Business Instgram Account  
    from graph api requirments, you can switch any account you have
  - Last longing access_token  
    Normal tokens expire in 30mins, follow graph api docs to get one
  - Valid token permissions  
    Not using the right permissions will fail the bot, follow  
    graph API docs to get the right permissions  
  - Telegram bot token  
    Optional, used for logging errors/status


### Railway
it's easier to deploy on railway, it has a deploy template everything is set up for you.
  - Click railway button
  - put your token/env in variables
  - enjoy!

### Heroku
  - click the heroku deploy button
  - make a new bot with bot father on telegram copy token
  - paste your token and other env, then deploy
  - enjoy!

### Local deploy
  - clone this repo
    `git clone https://github.com/Justxd22/iquote_xd && cd iquote_xd/`
  - install requirements with pip
    `pip install ./requirements.txt`
  - make and fill .env with your env (use .env.example)
  - run bot.py
    `python3 iquote.py`
  - enjoy!! :]

### Docker
i've setup up Dockerfile for you build the container and set your env  

# Credits

[justxd22/gquote](https://github.com/justxd22/gquote) - gen quote images from api

Big thanks to [zenquotes.io](https://zenquotes.io) for their amazing freeware api

pm on telegram for any queries [@Pine_Orange](t.me/Pine_Orange) or [@xd2222](t.me/xd2222)

instgram [@_.xd22](https://instagram.com/_.xd22)

find me [xd22.me](https://xd22.me)

# Donation
You can support my work by donating to the following address,

  - XMR - `433CbZXrdTBQzESkZReqQp1TKmj7MfUBXbc8FkG1jpVTBFxY9MCk1RXPWSG6CnCbqW7eiMTEGFgbHXj3rx3PxZadPgFD3DX` THANKS KIND SOUL!
