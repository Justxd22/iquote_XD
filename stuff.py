import os, json
from database import redis_connection

f = os.listdir()
if ".env" in f:
    env = open('.env', 'r').read()
    env = json.loads(env)
    # load env from json
    token  = env['token']
    tokenSP= env['token_splash']
    telet  = env['telet']
    telec  = env['telec']
    igID   = env['igID']
    redisU = env['redisURI']
    redisP = env['redisPASS']
    lc     = env['locationID'] # instgram location ids
else: # if not .env try enviroment vars
    token  = os.getenv('token', None)
    tokenSP= os.getenv('token_splash', None)
    telet  = os.getenv('telet', None)
    telec  = os.getenv('telec', None)
    igID   = os.getenv('igID', None)
    redisU = os.getenv('redisURI', None)
    redisP = os.getenv('redisPASS', None)
    lc     = os.getenv('locationID', None)

if not token or not igID:
    print('PLEASE SET token, igID IN .env FILE OR AS ENV VARS')
    exit(1)

lc = json.loads(lc) if lc else [100408319553597]

db = None
def init_db():
    db = redis_connection(redisU, redisP)
    return db
db = init_db()    

# init db if it's the first run
if db:
    n = db.get('nquotes')
    if not n: db.set('nquotes', 1)
    ol = db.get('OLDQ')
    if not ol: db.set('OLDQ', '{}')
    ol = db.get('OLDB')
    if not ol: db.set('OLDB', '{}')

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
# unsplash random collections
collections = [3672442, 214, 474028, 381380, 3333421, 932210, 11649432, 1599413, 1041983, 220381, 1410320, 540518, 17098, 467163, 443273]
