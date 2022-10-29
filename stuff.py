import os, json
from database import redis_connection

f = os.listdir()
if ".env" in f:
    env = open('.env', 'r').read()
    env = json.loads(env)
    # load env from json
    token = env['token']
    telet = env['telet']
    telec = env['telec']
    igID  = env['igID']
    redisU= env['redisURI']
    redisP= env['redisPASS']
else: # if not .env try enviroment vars
    token = os.getenv('token', None)
    telet = os.getenv('telet', None)
    telec = os.getenv('telec', None)
    igID  = os.getenv('igID', None)
    redisU= os.getenv('redisURI', None)
    redisP= os.getenv('redisPASS', None)

if not token or not igID:
    print('PLEASE SET token, igID IN .env FILE OR AS ENV VARS')
    exit(1)

db = redis_connection(redisU, redisP)
# init db if it's the first run
if db:
    n = db.get('nquotes')
    if not n: db.set('nquotes', 1)
    ol = db.get('OLDQ')
    if not ol: db.set('OLDQ', '{}')

cap  = """
⠀⠀⠀⠀⠀.　　　　　　　　　　⠀　　　　　　✦ 　　　　　,　　　　　　　.
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀☀️
　　　　　　*　　　　　　　　　　　.
.　　　　　　　　　　　　　. 　　✦⠀　   　　　,　　　　　　　　　*

　　　　　　　　　　　　　　　　　　.
　　　　.　　　　.　　　⠀🌖
　　　　　　　　　　　.
🚀
　　　˚　　　　　　　　ﾟ　　　　　.
　.⠀　　🌎⠀‍⠀‍⠀‍⠀‍⠀‍⠀‍⠀‍⠀‍⠀‍⠀‍⠀,
　　　*　　⠀.
　　　　　.　　　　　　　　　　⠀✦
　˚　　　　　　　　　　　　　　*
.⠀ 　　　　　　　　　　.

%23quotes %23xd_quote %23writers %23artist %23feelings %23lifequotes %23quoteoftheday %23spreadpositivity %23motivationoftheday %23positivityiskey %23inspiration %23inspirationalquotes %23motivationalquotesoftheday %23quotesofinstagram %23mindsetmatters %23wisdomquote %23quotestoliveby %23explore %233amquotes %23explorepage %23trending %23trendingnow %23dailylifequotes %23wisdom %23wordsofwisdom %23dailywisdom %23growth %23hviralquotes %23realshit"""
base = f"https://graph.facebook.com/v15.0/{igID}"
