import json, os, time, requests, base64, asyncio, signal
from threading import Thread as thrd
from gquote import gquote
from stuff import *

old        = " "
errors     = " "
nquotes    = None
old_quotes = None
lt         = None

# update DB
def updb(task=""):
    global lt, nquotes, old_quotes
    if task == "startup":
       nquotes    = int(db.get('nquotes')) # no. quotes
       old_quotes = json.loads(db.get('OLDQ'))
       lt         = int(db.get('lt').split('.')[0])
       return

    db.set('lt', lt)
    db.set('nquotes', nquotes)
    db.set('OLDQ', json.dumps(old_quotes))

# report stats to telegram
def stats(notes=None):
    print('called')
    msg = ""
    if notes:
       msg += f"*[{notes}]*"
       msg += f"\n*Posts*: {nquotes}"
       msg += f"\n*Last Post:* {timeinletters(lt)} ago"
       msg += f"\n*Next Post:* {timeinletters(lt+3600*5)}"
    if not notes or notes == "POSTED!":
       msg += "\n*=====POST DETAILS=====*"
       msg += "\n" + caption.replace('_', '\_')
       msg += "\n\n" + url.replace('_', '\_')
       msg += f"\n\n*ERRORS:*\n{errors}"
       if old != " ": msg += f"\n\n*Duplicates:*\n{old}"
    print(msg)
    # REPORT BACK ON TELEGRAM
    if not telet: print(msg)
    else:
        u = f"https://api.telegram.org/bot{telet}/sendMessage?chat_id={telec}&parse_mode=Markdown&text={msg}"
        try:
            t = requests.get(u)
            print(t.text)
        except Exception as e: print(e)


def timeinletters(unixt):
    h = 86400
    m = 3540
    s = 59
    t    = int(time.time())
    diff = abs(t - unixt)
    if   diff < s:  return str(diff) + "s"
    elif diff < m:  return str(round(diff/60)) + "m"
    elif diff < h:  return str(int(diff/3600)) + "h"
    else:           return str(int(diff/86400)) + "days"

# lt = last time posted in unix time format
async def iquote():
    global lt, nquotes, old_quotes, old, errors, caption, url
    if not lt: lt = 0 # if for any reason lt isnt set
    tt = 60*60*5   # target is 5 hours
    while 1:
       if int(time.time()) >= lt + tt: # last post time + five hours
           # only post if 5 hrs were passed
           while 1:
               # generate quote & check if it's new
               i = gquote(format="jpeg", output=False, shape="box")
               quote = i.run()
               # record quote in db to avoid duplicates
               text = base64.urlsafe_b64encode(bytes(i.quote, 'utf-8'))[:20].decode()
               try: is_old = old_quotes[text] # if raised TypeError then quote isnt in list
               except: is_old = False         # so it's a new quote
               if is_old:
                   old += "\n" + i.quote # for debugging purpose
                   continue # generate new quote
               else:
                   old_quotes[text] = 1 # record this quote in list as old
                   break

           # upload quote to bashupload
           # as instagram graph api requires photo url
           try: url = requests.put('https://bashupload.com', data=quote.getbuffer())
           except Exception as e:
               print(e, url.status_code)
               errors += "[ERROR]\n\n" + str(e)
               stats() # report error
               await asyncio.sleep(4)
               continue
           # the following done by absoulte noob
           url = url.text.replace('\n', '').replace('='*25, '').split("wget ")[1]
           # time to upload
           caption = f"%23{nquotes} by ~{i.author.replace('~','').replace(' ','')}\n{cap}"
           # try to post if any errors try again for x4 times
           mediaID = None
           for t in range(4):
               try:
                   if not mediaID:
                       mediaID = requests.post(base + f"/media?image_url={url}&caption={caption}&access_token={token}")
                       code    = mediaID.status_code, mediaID.text
                       if code[0] != 200:
                           mediaID = None
                           raise TypeError("BAD API "+str(code[0]) + '\n' + code[1])
                       mediaID = json.loads(mediaID.text)['id'] # mediaID is needed to publish
                   publish = requests.post(base + f"/media_publish?creation_id={mediaID}&access_token={token}")
                   if publish.status_code != 200: raise TypeError("BAD API PUBLISH "+publish.status_code)
                   else: break
               except Exception as e:
                   errors += "[ERROR]\n\n" + str(e)
                   await asyncio.sleep(4)
                   if t >= 3:
                       stats() # report error and try again
                       continue
                       # exit(1)
           nquotes += 1
           lt = int(time.time())
           updb()
           stats('POSTED!')
           continue
       else: # last post + five hours - current time = how much time to wait
           sleep = (lt + tt) - int(time.time())
           print('sleeping for', sleep)
           await asyncio.sleep(sleep)
           continue

def runasync(): # run thread in asyncio loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(iquote())

def handle(h, f):
    updb()
    stats('Shutdown')
    exit()

signal.signal(signal.SIGTERM, handle)
signal.signal(signal.SIGINT, handle)
signal.signal(signal.SIGQUIT, handle)
updb('startup')
stats('StartUP')
tsk = thrd(target=runasync)
tsk.start()
tsk.join() # join the main loop
