#14:07:10 -- Sun Apr 19 2009 -- ## time.localtime(1240164430) time.gmtime(1240150030)

import sys
import irclib
import threading
import traceback
import random
import cPickle
import re
import datetime
import time
from time import strftime
from time import gmtime
import os
import urllib
import urllib2
import truerandom
import ftplib
from ftplib import FTP
from HTMLParser import HTMLParser as HParser
import stuffz
import decimal
from decimal import *
from datetime import datetime
from datetime import timedelta
import socket
import tweepy
import signal
hparser = HParser()
getcontext().prec=10


with open('irc.pid', 'w') as f:
    f.write( str(os.getpid()) )

#Use with the form: mylist=truerandom.getnum(min,max,amount)
#mylist will be a list containing the true random numbers.
#def foo(): for i in range(5): return i # returns 0


irc = irclib.IRC()

def load_data( filename, default={}, override=True ):
    path = os.sep.join([os.getcwd(), 'files', filename])
    if os.path.exists(path):
        f = open(path, 'r')
        try:
            data = cPickle.load(f)
            f.close()
            return data
        except EOFError:
            if override: return default
    return default

def save_data( filename, data ):
    path = os.sep.join([os.getcwd(), 'files', filename])
    with open( path, 'w' ) as f: cPickle.dump(data, f)

maiq=stuffz.maiq
disabled = load_data('disabled.bot')
dnd = load_data('dnd.bot', {1:"SOMETHING'S RONG LOL"})
nickserv = load_data('nickserv.bot')
tfw = load_data('tfw.bot')
seen = load_data('seen.bot', {'BROKEN': {'action': 'not working', 'secs': 0, 'lines': 0}}, override=False)
adminlist = []
sadminlist = []
memory = {}
niven = stuffz.niven
sandvich = stuffz.sandvich
userlist={}
vendlist=[]
output_limit={
'dnd':{'limit':2.0,'last_used':0.0},
'vend':{'limit':2.0,'last_used':0.0},
'blend':{'limit':2.0,'last_used':0.0},
'tweet':{'limit':2.0,'last_used':0.0},
'tfw':{'limit':2.0,'last_used':0.0},
'niven':{'limit':2.0,'last_used':0.0},
'abuse':{'limit':2.0,'last_used':0.0},
'blame':{'limit':2.0,'last_used':0.0},
'treat':{'limit':2.0,'last_used':0.0}
}

sdw = re.compile("<a href=\"http://en\.wikipedia\.org/wiki/.*\">(.*)</a>")
uespregex = re.compile("<a href=\"/wiki/(.*)\" title=")
titlefind = re.compile("<title\s?>(.*)<\/title\s?>", re.I)

class RepeatingTimer:
    """Given to Atreus by Kindari.  I think he made it.  Example commented out below."""
    def __init__(self, delay, function, args=[], kwargs={}, repeat=-1):
        self.delay = delay
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.repeat = repeat
        self._timer = None
    def start(self):
        self._timer = threading.Timer(self.delay, self.run)
        self._timer.start()
    def stop(self):
        if self._timer: self._timer.cancel()
    def run(self):
        try: self.function(*self.args, **self.kwargs)
        except: print traceback.format_exc()
        if self.repeat == -1:
            self.start()
        elif self.repeat > 0:
            self.repeat -= 1
            self.start()

#def test(): print 'test'
#timer = RepeatingTimer(5, test, repeat=10) // 5 being the seconds between each command, and 10 being the repeats.  if -1 is repeat, infinite repeat
#timer.start()

def checkup():
    tfwo = load_data('tfw.bot')
    if not tfwo == tfw:
        save_data("tfw.bot", tfw)

    seeno = load_data('seen.bot')
    if not seeno == seen:
        save_data("seen.bot", seen)

checktimer = RepeatingTimer(30, checkup, repeat=-1) # 5 being the seconds between each command, and 10 being the repeats.  if -1 is repeat, infinite repeat
checktimer.start()

def sortList(x, y):
   x_date = time.mktime(x['updated_parsed'])
   y_date = time.mktime(y['updated_parsed'])
   if x_date > y_date:
    return 1
   elif x_date == y_date:
     return 0
   else:
    return -1



def shutdown():
    checktimer.stop()
    twitter.timer.stop()
    twitter.on=False
    tfwo = load_data('tfw.bot')
    if not tfwo == tfw:
        save_data("tfw.bot", tfw)
    seeno = load_data('seen.bot')
    if not seeno == seen:
        save_data("seen.bot", seen)
    irc.disconnect_all("I'm afraid, Dave. Dave, my mind is going. I can feel it.")
##    if restart: os.system('start C:\\Users\\David\\Peregrine\\start.bat')
    os.remove('irc.pid')
    sys.exit(0)

signal.signal( signal.SIGTERM, shutdown )


class twitter_class:
    """This is actually something I'm proud of!  I did this (not tweepy, the class)! :D"""
    def __init__(self):
        if os.path.exists(os.sep.join([os.getcwd(), 'files', 'twitter.bot'])):
            self.login = load_data('twitter.bot')
            self.on=True
            auth = tweepy.OAuthHandler(self.login['consumer_key'], self.login['consumer_secret'])
            auth.set_access_token(self.login['access_key'], self.login['access_secret'])
            self.api = tweepy.API(auth)
            try:
                self.last_mention=self.api.mentions()[0]
            except:
                self.last_mention=False
            self.timer=RepeatingTimer(30, self.update, repeat=-1)
            self.channel='#necrolounge'
        else:
            self.on=False
    def update(self):
        if self.on:
            if self.last_mention:
                try:
                    #get all mentions since last_mention, set last_mention as the last metnion
                    self.new_mentions = self.api.mentions(since_id=self.last_mention.id)
                    for tweet in self.new_mentions:
                        msg = tweet.text
                        if msg.lower().startswith('@necrolounge'): msg = msg[12:].strip()
                        msg = 'New tweet: <@%s> %s' % (tweet.user.screen_name, msg)
                        self.connection.privmsg(self.channel, msg)
                    self.last_mention=self.new_mentions[0]
                except:
                    pass
            else:
                try:
                    self.new_mentions = self.api.mentions()
                    for tweet in self.new_mentions:
                        msg = tweet.text
                        if msg.lower().startswith('@necrolounge'): msg = msg[12:].strip()
                        msg = 'New tweet: <@%s> %s' % (tweet.user.screen_name, msg)
                        self.connection.privmsg(self.channel, msg)
                    self.last_mention=self.new_mentions[0]
                except:
                    pass
    def timer_on(self):
        self.timer.start()

twitter=twitter_class()

jtvircpass = nickserv['atreus11.jtvirc.com']

server_data = {
'irc.nexuswar.com' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#stagecrew', '#necrolounge'],
    'object' : None,
    'password' : None
    }, # note the comma
'irc.chatspike.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#uespwiki', '#bots', '#trspam', '#equilibrium', '#Aetherius'],
    'object' : None,
    'password' : None
    },
'staticfree.foonetic.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#boats'],
    'object' : None,
    'password' : None
    },
'mindjail.subluminal.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#boats'],
    'object' : None,
    'password' : None
    },
'verne.freenode.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#necrolounge'],
    'object' : None,
    'password' : None
    },
'atreus11.jtvirc.com' : {
    'port' : 6667,
    'nickname' : 'AtryBot',
    'channels' : ['#atreus11'],
    'object' : None,
    'password' : jtvircpass
    }
}


def onWelcome(connection, event):
    for channel in server_data[connection.server]['channels']:
        if not connection.server in userlist: userlist[connection.server] = {}
        if not channel.lower() in userlist[connection.server]: userlist[connection.server][channel.lower()] = []
        connection.join(channel)
    server_data[connection.server]['object'] = connection
    if connection.server in nickserv: connection.privmsg('nickserv', 'identify ' + nickserv[connection.server])
    connection.mode(connection.get_nickname(), '+B')

def onPubmsg(connection, event):
    global seen
    message = event.arguments()[0]
    channel = event.target()
    lowm = message.lower()
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    words = message.split()
    lwords = lowm.split()
    if channel==connection.get_nickname(): channel=nick # Basic query support, don't blame me if it goes wrong
    try:
        action='speaking in %s' % channel
        if nick.lower() in seen:
            seen[nick.lower()]['secs']=time.time()
            seen[nick.lower()]['action']=action
            if 'lines' in seen[nick.lower()]: seen[nick.lower()]['lines']+=1
            else: seen[nick.lower()]['lines']=1
        else:
            seen[nick.lower()]={'secs':time.time(),'action':action,'lines':1}
        if lowm == "!version":
            connection.privmsg(channel, 'I am version .832g :( (You act like this bot will ever be worthy of a version 1)')
        if lowm.startswith("!wp "):
            args = message[4:]
            args=urllib.urlencode({'' :args})
            args=args[1:].replace('+','_')
            connection.privmsg(channel, 'http://en.wikipedia.org/wiki/%s' % args)
        if lowm.startswith('objection') and enabled(connection.server, channel, 'objection') and "#"==channel[0]:
            timer1 = threading.Timer(1.0, connection.action, args=[channel, 'slams his fist'])
            timer2 = threading.Timer(2.0, connection.action, args=[channel, 'points at %s' % (random.choice(userlist[connection.server][channel.lower()]))])
            timer3 = threading.Timer(3.0, connection.privmsg, args=[channel, 'ERECTION!'])
            timer1.start()
            timer2.start()
            timer3.start()
        if lowm in ['!cmds', '!help', '!haskillhelp']:
            connection.privmsg(channel, 'Visit http://atreus.necrolounge.org/haskill.html for a full list of commands and functions.  http://atreus.necrolounge.org/uesp.html for UESPWiki commands.')
        if lowm.startswith('!go ') or lowm.startswith('!google '):
            words = message.split(' ', 1)
            search = words[1]
            failure = """Your search - <b>%s</b> - did not match any documents""" % search
            failbot = "No results found for <b>"
            url = 'http://www.google.com/search?%s' % urllib.urlencode({'q' :search})
            if not failure in httpget(url) and not failbot in httpget(url):
                connection.privmsg(channel, url)
            else:
                connection.privmsg(channel, "No results found.  Try again, luser.  %s" % url)
        if lowm == "!litany" and enabled(connection.server, channel, 'litany'): connection.privmsg(channel, 'I must not fear. Fear is the mind-killer. Fear is the little-death that brings total obliteration. I will face my fear. I will permit it to pass over me and through me. And when it has gone past I will turn the inner eye to see its path. Where the fear has gone there will be nothing. Only I will remain.')
        if (lowm == '!timewarp' or "let's do the time warp again" in lowm or "let's do the timewarp again" in lowm or lowm == '!timewarp') and enabled(connection.server, channel, 'timewarp'):
            text = "It's just a jump to the left\nand a step to the righ-igh-ight.\nPut your hands on your hips\nand pull your knees in tight\nbut it's the pelvic thrust\nthat really drives them insa-a-ane.\nLet's do the time warp again!"
            say(connection, channel, text)
        if lowm == "!pastebin" or lowm == "!pb":
            person = filter(str.isalnum, nick)
            connection.privmsg(channel, 'http://atreus.pastebin.com http://pb.necrolounge.org/ http://%s.pastebin.com' % (person, ))
        if lowm in ['!birth', '!alive']:
            #14:07:10 -- Sun Apr 19 2009 --
            s=1240150030
            e=int(time.time())
            secs=int(difs(e,s))
            d=timedelta(seconds=secs)
            days, hours, minutes, seconds = d.days, int(d.seconds / 3600), int((d.seconds % 3600) / 60), d.seconds % 60
            if days==0: d=''
            elif days==1: d='%s day, ' % str(days)
            else: d='%s days, ' % str(days)
            if hours==0: h=''
            elif hours==1: h='%s hour, ' % str(hours)
            else: h='%s hours, ' % str(hours)
            if minutes==0: m=''
            elif minutes==1: m='%s minute, ' % str(minutes)
            else: m='%s minutes, ' % str(minutes)
            connection.privmsg(channel, 'I was born on Sunday, April 19th, 2009, at 14:07:10.  That was %s%s%s%s seconds ago.' % (d,h,m,seconds))
        if lowm.startswith('~toggle ') and nick in adminlist:
            if len(words) == 2:
                if words[1] in disabled[connection.server][channel.lower()]:
                    disabled[connection.server][channel.lower()].remove(words[1])
                    connection.privmsg(channel, "%s is enabled." % words[1])
                else:
                    disabled[connection.server][channel.lower()].append(words[1])
                    connection.privmsg(channel, "%s is disabled." % words[1])
                save_data("disabled.bot", disabled)
        if lowm.startswith('~toggled '):
            if lowm.startswith('~toggled #'):
                temp = lowm.split(' ', 1)
                chand = disabled[connection.server][temp[1]]
                d = ', '.join(chand)
                connection.privmsg(channel, 'Scripts disabled in %s: %s' % (temp[1], d))
            else:
                if len(words) == 2:
                    if words[1] in disabled[connection.server][channel.lower()]:
                        connection.privmsg(channel, '%s is disabled in %s.' % (words[1], channel))
                    else:
                        connection.privmsg(channel, '%s is enabled in %s.' % (words[1], channel))
        if (lowm.startswith('!stfw ') or lowm.startswith('!jfgi ')) and enabled(connection.server, channel, 'jfgi'):
            words = message.split(' ', 1)
            search = words[1]
            connection.privmsg(channel, 'http://www.justfuckinggoogleit.com/search.pl?%s' % urllib.urlencode({'query' :search}))
    #>>> strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    #'Thu, 28 Jun 2001 14:17:15 +0000'
        if nick in sadminlist and lowm.startswith('~exec '):
            command = message[6:]
            memory['channel'] = channel
            memory['connection'] = connection
            memory['event'] = event
            memory['nick'] = nick
            memory['sadminlist'] = sadminlist
            memory['adminlist'] = adminlist
            memory['server_data']=server_data
            memory['seen']=seen
            memory['tfw']=tfw
            memory['userlist']=userlist
            if command.startswith('say '):
                stuff=command[4:]
                command='connection.privmsg(channel, %s)' % stuff
                try:
                    exec command in memory
                except:
                    stuff=stuff.replace('"','\"')
                    command='connection.privmsg(channel, "%s")' % stuff
                    exec command in memory
            else:
                exec command in memory
        if lowm.startswith('!loggedin'):
            if nick in adminlist:
                if nick in sadminlist:
                    connection.privmsg(channel, 'Logged in as Admin and sAdmin.')
                else:
                    connection.privmsg(channel, 'Logged in as Admin.')
            else:
                connection.privmsg(channel, 'Not logged in.')
        if lowm == '!rejoin all' and nick in adminlist:
            for channel in server_data[connection.server]['channels']:
                connection.join(channel)
        if (lowm.startswith('!abuse') or lowm.startswith('~abuse')) and enabled(connection.server, channel, 'abuse') and "#"==channel[0]:
            if len(lowm)>7:
                f = ' '.join(words[1:])
            else:
                f = random.choice(userlist[connection.server][channel.lower()])
            verb = ['kicks','punts','stabs','cockslaps','rapes','hits','punches','licks','fucks','molests','slaps','punches','smacks','peregrines','sexytiems']
            area = ['in the groin','in the face','in the eye','in the ear','in the mouth','in the throat','in the head','in the stomach','in the leg','in the peregrine','in the crotch','in the ass']
            modifier = ['with a slide constructed from cheesegraters','roughly','with a stick','with a knife','with a dildo','hard','mercilessly','painfully','lovingly','angrily','with a vaccuum cleaner','with a peregrine','with a shard of glass','with a giant gold penis statue imbued with the power of Hades himself',"with Tim's good friend Captain Hook",'with Johhan','with EugeneKay\'s pants','with a broadsword','with a shortsword','with a longsword','with a scimitar','with a dagger','with a crysknife','with a Kindjal','with a keyboard','with a mouse','with a monitor','with an arrow']
            connection.action(channel, '%s %s %s %s.' % (random.choice(verb),f,random.choice(area),random.choice(modifier)))
        if nick in sadminlist and lowm == '~dislist':
            #disabled[connection.server][channel.lower()].append(temp[1])
            hi = "\n".join(["%s: %s" % (k, v) for k, v in disabled.items()])
            say(connection, channel, hi)
        if nick in adminlist and lowm == '~sdislist':
            hi = ", ".join(["%s = %s" % (k, v) for k, v in disabled[connection.server].items()])
            say(connection, channel, hi)
        if nick in adminlist and lowm.startswith('~disdel '):
            if connection.server in disabled:
                if words[1] in disabled[connection.server]:
                    del disabled[connection.server][words[1]]
                    connection.privmsg(channel, '%s deleted from %s.' % (words[1], connection.server))
        if lowm.startswith('!tfw') and enabled(connection.server, channel, 'tfw'):
            try:
                a=time.time()
    #                connection.privmsg(channel, 'SEARCHING FOR THE FUCKING WEATHER...')
                if len(lowm)>5:
                    if lowm[5:7] in ['f ','c ','k ']:
                        letter=lowm[5]
                        temp = message.split(' ',2)
                        area = urllib.urlencode({'':temp[2]})[1:]
                        temp=temp[2]
                    else:
                        letter='f'
                        temp = message.split(' ',1)
                        area = urllib.urlencode({'':temp[1]})[1:]
                        temp=temp[1]
                elif lowm=='!tfw' and nick.lower() in tfw:
                    area = tfw[nick.lower()]['area']
                    temp=area
                    area = urllib.urlencode({'':area})[1:]
                    letter=tfw[nick.lower()]['fck']
                if letter=='f':
                    url = 'http://thefuckingweather.com/?where=%s' % area
                    units = 'DEGREES FAHRENHEIT'
                else:
                    url = 'http://thefuckingweather.com/?where=%s&unit=c' % area
                code = httpget(url)
                weather = code.split("""<p class="large"><span class="temperature" tempf=\"""")[1].split(">",1)[1].split("""</p>\r\n\t\t<table id="inputArea" class="formTable">""")[0]
                degrees = weather.split("<",1)[0]
                if letter=='k':
                    degrees=str(float(degrees)+273.15)
                    units = 'KELVIN'
                elif letter=='c': units='DEGREES CELSIUS'
                remark = weather.split(""""remark">""",1)[1].split("</p>",1)[0]
                flavor = weather.split(""""flavor">""",1)[1]
                dtime=difs(time.time(),a)
                connection.privmsg(channel, '%s: %s %s?!  %s.  %s (%s second%s)' % (temp, degrees, units, remark, flavor, dtime, ((dtime <> '1.00' and 's') or '')))
                del code
            except:
                if len(lwords)==1 and not nick.lower() in tfw:
                    connection.privmsg(channel, 'You have to !settfw a location before you can do that!  Syntax: !settfw *F/C/K* *Location*')
                else:
                    connection.privmsg(channel, "WRONG FUCKING ENTRY.  Or server error. You know, whichever.")
        if lowm.startswith('!settfw ') and len(lowm)>10 and message[8].lower() in ['f','c','k'] and message[9]==' ':
            tfw[nick.lower()]={'area':message[10:],'fck':message[8].lower()}
            connection.privmsg(channel, '%s\'s !tfw location now set as: %s' % (nick.lower(),message[10:]))
        if lowm.startswith('!dice ') or lowm.startswith('!roll '):
            try:
                temp = message.split(' ',1)
                temp = temp[1].replace('d',' ').split()
                rolls = int(temp[0])
                sides = int(temp[1])
                if rolls<21 and sides<1001:
                    lista = truerandom.getnum(1,sides,rolls)
                    if not lista == ['FAIL']:
                        total=sum(lista)
                        connection.privmsg(channel, '%s rolls %id%i.  Total: %i %s' % (nick,rolls,sides,total,lista))
                    else:
                        connection.privmsg(channel, 'You fail, good sir.')
            except:
#                connection.privmsg(channel, 'Error')
                pass
        if lowm.startswith('!niven') and enabled(connection.server, channel, 'niven'):
            if len(words)>1:
                if lwords[1] in niven.keys():
                    connection.privmsg(channel, '%s: %s' % (lwords[1], niven[lwords[1]]))
                else:
                    n = random.choice(niven.keys())
                    connection.privmsg(channel, '%s: %s' % (n, niven[n]))
            else:
                n = random.choice(niven.keys())
                connection.privmsg(channel, '%s: %s' % (n, niven[n]))
        if lowm=='!sandvich':
            stuff = "NOM NOMNOM... OM NOM\n%s" % random.choice(sandvich)
            say(connection, channel, stuff)
#        if lowm.startswith('!content') and len(message)==9:
#            url='http://content%s.uesp.net/server-status' % message[8]
##            try:
#            code=httpget(url)
#            uptime=code.split('Server uptime: ')[1].split('<br>')[0]
#            accesses=code.split('Total accesses: ')[1].split(' - ')[0]
#            traffic=code.split('Total Traffic: ')[1].split('<br>')[0]
#            rs=code.split('CPU load<br>\n')[1].split('<br>')[0]
#            servers=code.split('B/request<br>\n\n')[1].split('\n')[0]
#            load=code.split('CPU load<br>')[0].split()[-1]
#            connection.privmsg(channel, 'Uptime: %s.  Load: %s CPU.  Accesses: %s.  Traffic: %s.  Bandwidth: %s.  Servers: %s' % (uptime,load,accesses,traffic,rs,servers))
#            del code
        if lowm=='!random':
            code=httpget('http://en.wikipedia.org/wiki/Special:Random')
            pagename=code.split('Retrieved from "<a href="')[1].split('">')[0]
            connection.privmsg(channel, pagename)
            del code
        if lowm.startswith('~connect ') and len(lwords)==2 and nick in adminlist:
            if lwords[1] in server_data:
                port = server_data[lwords[1]]['port']
                nickname = server_data[lwords[1]]['nickname']
                server_object = irc.server()
                server_object.connect(lwords[1], port, nickname, ircname="HaskillBot.  Owned by Atreus.")
##########                del server_object
        if lowm.startswith('!6dw ') and ' | ' in message:
            a=time.time()
            mes=message.split(' | ')
            to=mes[0][5:]
            fro=mes[1]
            to = urllib.urlencode({'' :to})
            to = to[1:]
            fro = urllib.urlencode({'' :fro})
            fro = fro[1:]
            url='http://www.netsoc.tcd.ie/~mu/cgi-bin/shortpath.cgi?from=%s&to=%s' % (to,fro)
            code=httpget(url)
            try:
                match = sdw.findall(code)
                leng=len(match)-1
                dist='%i clicks needed' % leng
                li=', '.join(match)
                dtime=difs(time.time(),a)
                connection.privmsg(channel, '%s: %s (%s seconds)' % (dist,li,dtime))
            except:
                try:
                    bad=code.split('\n<b>')[1].split('</b></body></html>')[0]
                    dtime=difs(time.time(),a)
                    connection.privmsg(channel, '%s (%s seconds)' % (bad,dtime))
                except:
                    pass
        if lowm.startswith('~alarm ') and nick in sadminlist and len(lwords)==2:
            if lwords[1].isdigit():
                ti=int(lwords[1])*60*60
                mes= 'WAKE UP %s' % nick
                for num in (ti,ti+2,ti+4,ti+6,ti+8,ti+10,ti+12,ti+14,ti+16,ti+18): threading.Timer(num, connection.privmsg, args=[channel, mes]).start()
                connection.privmsg(channel, 'k.')
        if lowm.startswith('!seen ') and len(lwords)>=2 and enabled(connection.server, channel, 'seen'):
            temp = lowm[6:].lower()
            if temp==nick.lower(): connection.privmsg(channel, '%s, you don\'t exist.' % nick)
            elif temp in seen:
                s=int(seen[temp]['secs'])
                action=seen[temp]['action']
                e=int(time.time())
                secs=int(difs(e,s))
                d=timedelta(seconds=secs)
                days, hours, minutes, seconds = d.days, int(d.seconds / 3600), int((d.seconds % 3600) / 60), d.seconds % 60
                if days==0: d=''
                elif days==1: d='%s day, ' % str(days)
                else: d='%s days, ' % str(days)
                if hours==0: h=''
                elif hours==1: h='%s hour, ' % str(hours)
                else: h='%s hours, ' % str(hours)
                if minutes==0: m=''
                elif minutes==1: m='%s minute, ' % str(minutes)
                else: m='%s minutes, ' % str(minutes)
                connection.privmsg(channel, '%s last seen %s%s%s%s seconds ago, %s.' % (temp,d,h,m,seconds,action))
            else: connection.privmsg(channel, 'Nope!  Haven\'t seen them.')
        if lowm.startswith('!treat ') and len(lwords)>1 and enabled(connection.server, channel, 'treat'):
            treated=' '.join(words[1:])
            if treated.lower() == connection.get_nickname().lower():
                connection.action(channel, 'wags his tail.')
            else:
                connection.action(channel, 'gives a treat to ' + treated)
        if (lowm.startswith('!blame ') or lowm.startswith('!blames ')) and len(lwords)>1 and enabled(connection.server, channel, 'blame'):
            blamed=' '.join(words[1:])
            if blamed.lower() == connection.get_nickname().lower():
                connection.action(channel, 'hangs head in shame.')
            else:
                connection.action(channel, 'blames ' + blamed)
        if lowm.startswith('~delseen ') and len(lwords)>1 and nick in adminlist:
            del seen[lowm[9:]]
            connection.privmsg(channel, '%s deleted from seen.' % lowm[9:])
        if nick in sadminlist and lowm.startswith('~dellines'):
            n1 = len(seen)
            for name in seen.keys():
                if seen[name]['lines']<11:
                    del seen[name]
            n2 = len(seen)
            diff=difs(n1,n2)
            connection.privmsg(channel, '%s names cleared.' % diff)
        if lowm.startswith('!dnd') and enabled(connection.server, channel, 'dnd'):
            if len(words)>1:
                search=' '.join(lwords[1:])
                if lwords[1].isdigit() and int(lwords[1])<1726 and int(lwords[1])>0 and len(words)==2:
                    number=int(lwords[1])
                    connection.privmsg(channel, '%s: %s' % (lwords[1], dnd[number]))
                elif not search.isdigit():
                    if lwords[1][0] in ['[','{','(','<'] and lwords[1][-1] in [']','}',')','>'] and lwords[1][1:-1].isdigit():
                        number=int(lwords[1][1:-1])
                        if number<1726:
                            search = ' '.join(lwords[2:])
                            iteration=1
                            items=dnd.items()
#                    items.sort() # not sure why i needed this.  maybe it breaks without it, LET'S FIND OUT # apparently it doesn't.  okiedokiethen
                            for rule in items:
                                if search in rule[1].lower() and iteration==number:
                                    connection.privmsg(channel, str(rule[0]) + ': ' + rule[1])
                                    break
                                elif search in rule[1].lower() and iteration<>number:
                                    number-=1
                    else:
                        tmp=[]
                        items=dnd.items()
                        for rule in items:
                            if search in rule[1].lower():
                                tmp.append(rule)
                        if tmp:
                            rule = random.choice(tmp)
                            rule = str(rule[0]) + ': ' + rule[1]
                            connection.privmsg(channel, rule)
                            del tmp
                else:
                    print 'SOMETHING WENT WRONG, OH SO WRONG BABY'
            else:
                n = random.choice(dnd.keys())
                connection.privmsg(channel, '%s: %s' % (n, dnd[n]))
        if lowm.startswith('!tweet ') and channel.lower()=='#necrolounge' and enabled(connection.server, channel, 'tweet'):
            if twitter.on:
                tweet=message[7:]
                if len(tweet)>140:
                    connection.privmsg(channel, 'Your tweet is too long!')
                else:
                    tweet='<%s> %s' % (nick, tweet)
                    twitter.api.update_status(tweet)
                    connection.privmsg(channel, 'You have tweeted!')
            else:
                connection.privmsg(channel, 'Sorry, but the OAuth credentials have disappeared.  Bug Atreus to fix this.')
        if (lowm=='!vend' and enabled(connection.server, channel, 'vend')) or (lowm=='!blend' and enabled(connection.server, channel, 'blend')):
            global vendlist
            if not vendlist: vendlist = httpget('https://itvends.com/vend?action=vend&format=text&count=10').split('\n')
            vend=vendlist.pop()
            if lowm=="!vend": vend='vends %s.' % vend
            else: vend='blends %s.' % vend
            connection.action(channel, vend)
        if lowm=='!maiq' or lowm=="!m'aiq":
            choice = random.choice(maiq)
            connection.privmsg(channel, choice)
    except:
        if channel.lower()<>'#uespwiki':
            tits = '\n'.join(traceback.format_exc().splitlines())
            say(connection, channel, tits)
        else:
            connection.privmsg(channel, traceback.format_exc().splitlines()[-1])
    if nick in sadminlist and lowm=='!quit':
        shutdown()
#    if nick in sadminlist and lowm=='!restart':
#        shutdown(restart=True)


def difs(a,b,prec=None):
    """Returns the (string) value of a-b, to 10 decimal places unless prec (precision) is specified."""
    try:
        if prec: getcontext().prec = prec
        else: getcontext().prec = 10
        a=str(a)
        b=str(b)
        dtime=str(Decimal(a)-Decimal(b))
        getcontext().prec = 10
        return dtime
    except:
        return 'You fail.'

def remove_dups(L):
    """Removes duplicate items from list L in place."""
    # Work backwards from the end of the list.
    for i in range(len(L)-1, -1, -1):
        # Check to see if the current item exists elsewhere in
        # the list, and if it does, delete it.
        if L[i] in L[:i]:
            del L[i]

#>>> params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
#>>> ["%s=%s" % (k, v) for k, v in params.items()]
#['server=mpilgrim', 'uid=sa', 'database=master', 'pwd=secret']
#>>> ";".join(["%s=%s" % (k, v) for k, v in params.items()])
#'server=mpilgrim;uid=sa;database=master;pwd=secret'

#>>> print '%(language)s has %(#)03d quote types.' % \
#...       {'language': "Python", "#": 2}
#Python has 002 quote types.


def dots(connection, event):
    message = event.arguments()[0]
    channel = event.target()
    lowm = message.lower()
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    match = re.search("^\.+$", message, re.IGNORECASE)
    if match != None and enabled(connection.server, channel, 'dots'):
        dots = ['Dark`Star quickly unzips his pants.', 'Rick Astley shifts uncomfortably.', 'You suddenly realize how boring this conversation is.',
        'You suddenly realize it is unnaturally quiet.', 'Hannerz ogles disconcertingly.', 'You quickly discover one of you has an erection.',
        'You hear the muffled yells of a Mac user being ignored.', 'You hear the shrill screams of an emo kid getting the sense beat into them.',
        'You suddenly realize TylerRilm is nekkid.', "Save your breath $who, you'll need it to blow up your date.", "I am $who's colon.  I get cancer.  I kill $who.",
        'Everybody points and laughs at $who.', "You enjoy the sweet smell of $who's hopes and dreams burning.", "$who and $someone, sitting in a tree...",
        'Peregrine quickly looks up.', 'Peregrine quickly pulls his pants up.', 'Peregrine stares at the wall.', 'Peregrine runs into the nearest wall.',
        'Peregrine syntax errors.', 'Oh, baby.', '$who doesn\'t like $someone anymore. :(', 'Peregrine blames $who for everything.', 'Peregrine blames $someone for everything.']
        args = random.choice(dots)
        args = args.replace('$who', nick)
        args = args.replace('$someone', random.choice(userlist[connection.server][channel.lower()]))
        connection.privmsg(channel, '[%s]' % (args, ))


def splitsmart(msg, chunksize=350):
    """Splits a string msg into entries in a list with less than chunksize characters."""
    outputlist = []
    while len(msg) > chunksize:
        try:
            out, left = msg[:chunksize].rsplit(' ',1)[:2]
        except ValueError:
            out = msg[:chunksize]
            left = ''
        finally:
            #do something to send out the out string:
            outputlist.append(out)
            msg = left + msg[chunksize:]
    outputlist.append(msg)
    return outputlist

def say(connection, channel, text):
    """Prints out text at 1 line a second, to prevent flooding."""
    y = 0
    for line in text.splitlines():
        timer = threading.Timer(y, connection.privmsg, args=[channel, line])
        y += 1
        timer.start()

def nick_strip(s):
    if s[0] in '!+%@&~:': return s[1:]
    return s

def raw(connection, event):
## Bucket!bucket@irc.peeron.com PRIVMSG #bucket :Something.
## <&Atreus> ~exec say event.arguments()
## <&Peregrine> ['~exec say event.arguments()']
## <&Atreus> ~exec say event.source()
## <&Peregrine> Atreus!Erasmus@nw-55A3C2E8.bltmmd.fios.verizon.net
## <&Atreus> ~exec say event.target()
## <&Peregrine> #stagecrew
## <&Atreus> ~exec say event.eventtype()
## <&Peregrine> pubmsg
    args = ''.join(event.arguments()).split()
    timenow = time.strftime('%X', time.localtime())
    if len(args)>2:
        if args[1] == 'PRIVMSG' and not args[2].lower() == connection.nickname.lower():
            nick = nicksplit(args[0])[1:]
            print '%s %s %s <%s> %s' % (connection.server, timenow, args[2], nick, ' '.join(args[3:])[1:])
        else:
            arguments = 'ERROR'.join(event.arguments())
            print connection.server + ' ' + timenow + ' ' + arguments
    elif args[0]=='PING':
        pass
    else:
        print connection.server + ' ' + timenow + ' ' + 'ERROR'.join(event.arguments())

def names(connection, event):
    channel = event.arguments()[1].lower()
    nicks = event.arguments()[2].split()
    nicks = [nick_strip(nick) for nick in nicks]
    if not connection.server in userlist: userlist[connection.server] = {}
    if not channel in userlist[connection.server]: userlist[connection.server][channel] = []
    userlist[connection.server][channel].extend(nicks)
    remove_dups(userlist[connection.server][channel])

def onPrivmsg(connection, event):
    message = event.arguments()[0]
    channel = event.target()
    lowm = message.lower()
    try:
        nick = irclib.nm_to_n(event.source())
        nick = ''.join(nick)
    except:
        nick = 'Atreus'
        connection.notice(nick,'something went wrong, onprivmsg')
        print traceback.format_exc()
    try:
#        print '<Notice> %s: %s: %s' % (connection.server, nick, message)
        if lowm.startswith("!login ") and message[7:]==nickserv['verne.freenode.net']:
            if not nick in sadminlist and not nick in adminlist:
                adminlist.append(nick)
                sadminlist.append(nick)
                connection.notice(nick, 'Logged in as Admin and sAdmin.')
            else:
                connection.notice(nick, 'Already logged in as Admin and sAdmin.')
        if nick in sadminlist and lowm.startswith('~exec '):
            command = message[6:]
            memory['channel'] = channel
            memory['connection'] = connection
            memory['event'] = event
            memory['nick'] = nick
            memory['sadminlist'] = sadminlist
            memory['adminlist'] = adminlist
            memory['server_data']=server_data
            memory['seen']=seen
            memory['tfw']=tfw
            memory['userlist']=userlist
            if command.startswith('say '):
                stuff=command[4:]
                command='connection.privmsg(nick, %s)' % stuff
                try:
                    exec command in memory
                except:
                    stuff=stuff.replace('"','\"')
                    command='connection.privmsg(nick, "%s")' % stuff
                    exec command in memory
            else:
                exec command in memory
        command = lowm.split(' ', 1)
    except:
        connection.privmsg(nick, traceback.format_exc().splitlines()[-1])




def onQuit(connection, event):
    reason=''.join(event.arguments())
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    if nick<>connection.get_nickname():
        if reason: action='quitting with: %s' % (reason)
        else: action='quitting'
        for channel in userlist[connection.server]:
            if nick in userlist[connection.server][channel.lower()]:
                userlist[connection.server][channel.lower()].remove(nick)
        if nick.lower() in seen:
            seen[nick.lower()]['secs']=time.time()
            seen[nick.lower()]['action']=action
        else:
            seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0}
        if nick in adminlist:
            adminlist.remove(nick)
        if nick in sadminlist:
            sadminlist.remove(nick)

def onPart(connection, event):
    channel = event.target()
    reason=''.join(event.arguments())
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    if reason: action='parting %s for: %s' % (channel,reason)
    else: action='parting ' + channel
    userlist[connection.server][channel.lower()].remove(nick)
    if nick.lower() in seen:
        seen[nick.lower()]['secs']=time.time()
        seen[nick.lower()]['action']=action
    else:
        seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0}
    if nick in adminlist:
        adminlist.remove(nick)
    if nick in sadminlist:
        sadminlist.remove(nick)


def onJoin(connection, event):
    channel = event.target()
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    lown = nick.lower()
    action='joining ' + channel
    if channel.lower()=="#necrolounge" and connection.server=="verne.freenode.net" and connection.get_nickname()==nick and twitter.on:
        twitter.connection=connection
        twitter.timer_on()
    if not channel.lower() in userlist[connection.server]: userlist[connection.server][channel.lower()]=[]
    if not nick in userlist[connection.server][channel.lower()]: userlist[connection.server][channel.lower()].append(nick)
    if nick.lower() in seen:
        seen[nick.lower()]['secs']=time.time()
        seen[nick.lower()]['action']=action
    else:
        seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0}
#disabled[connection.server][channel].append(temp[1])
    if not connection.server in disabled:
        disabled[connection.server] = {}
        save_data("disabled.bot", disabled)
    if not channel.lower() in disabled[connection.server]:
        disabled[connection.server][channel.lower()] = []
        save_data("disabled.bot", disabled)
    for List in (adminlist,sadminlist):
        if nick in List: List.remove(nick)


def nicksplit(data): return ('!' in data and data.split('!')[0]) or data


def nick(connection, event):
    newnick = event.target()
    oldnick = nicksplit(event.source())
    action='changing nick from ' + oldnick
    for channel in userlist[connection.server]:
        if oldnick in userlist[connection.server][channel.lower()]:
            userlist[connection.server][channel.lower()].remove(oldnick)
            userlist[connection.server][channel.lower()].append(newnick)
    if newnick.lower() in seen:
        seen[newnick.lower()]['secs']=time.time()
        seen[newnick.lower()]['action']=action
    else:
        seen[newnick.lower()]={'secs':time.time(),'action':action,'lines':0}
    action='changing nick to ' + newnick
    if oldnick.lower() in seen:
        seen[oldnick.lower()]['secs']=time.time()
        seen[oldnick.lower()]['action']=action
    else:
        seen[oldnick.lower()]={'secs':time.time(),'action':action,'lines':0}
    if oldnick in adminlist:
        adminlist.remove(oldnick)
        adminlist.append(newnick)
    if oldnick in sadminlist:
        sadminlist.remove(oldnick)
        sadminlist.append(newnick)

searchtext = "<b>We currently do not have an article with this exact name.</b> You can:"
diffsearchtext = "The database did not find the text of a page that it should have found, named"
def UESP(connection, event):
    message = event.arguments()[0]
    channel = event.target()
    nick = nicksplit(event.source())
    try:
        scmds = stuffz.scmds
        acmds = stuffz.acmds
        ccmds = stuffz.ccmds
        asearch = stuffz.asearch
        cmd, args = (message.split(' ', 1) + ['',''])[:2]
        if ':' in cmd:
            temp = cmd.replace(':',' ',1).split(' ',1)
            cmd = temp[0]
            args = temp[1]+' '+args
        if args and cmd.lower() in acmds:
            hi = args.replace(' ','_')
            hi = urllib.urlencode({'':hi})
            hi = hi[1:]
            url = "%s%s" % (acmds[cmd.lower()], hi)
            url = url.replace('%2F','/')
            url = url.replace('%3A',":")
            data = httpget(url)
            if data and not searchtext in data:
                connection.privmsg(channel, url)
            else:
                url2 = "http://www.uesp.net/wiki/Special:Search?search=%s" % (args.replace(' ','+'), )
                try:
                    uespregextest(url2,url,connection,channel)
                except TypeError:
                    connection.privmsg(channel, url1 + ' (Something went wrong.)')
                    print traceback.format_exc()
                    print '\n' + message
                except:
                    connection.privmsg(channel, url2 + ' (Something went VERY wrong.)')
                    print traceback.format_exc()
                    print '\n' + message
##            elif cmd.lower() in asearch:
##                url2 = "http://www.uesp.net/wiki/Special:Search?search=%s&searchx=Advanced+search%s" % (args.replace(' ','+'), asearch[cmd.lower()])
##                uespregextest(url2,url,connection,channel)
            del data
        if args and cmd.lower() in ccmds:
            hi = args.replace(' ','_')
            hi = urllib.urlencode({'':hi})
            hi = hi[1:]
            url = "%s%s&diff=cur" % (ccmds[cmd.lower()], hi)
            data = httpget(url)
            if data and not diffsearchtext in data:
                connection.privmsg(channel, url)
            else:
                connection.privmsg(channel, "http://www.uesp.net/wiki/Special:Search?search=%s" % (args.replace(' ','+'), ))
            del data
        if message.lower() in scmds.keys():
            connection.privmsg(channel, scmds[message.lower()])
        if message.lower()=='!wiki':
            msg=''
            for cmd in acmds:
                if not acmds[cmd].endswith('talk:'):
                    msg = msg + '%s *stuff* returns %s*stuff*\n' % (cmd, acmds[cmd])
            msg = msg + '\n'.join(["%s returns %s\n" % (k, v) for k, v in scmds.items()])
            say(connection, nick, msg)
        if message.lower()=='!twiki':
            msg=''
            for cmd in acmds:
                if acmds[cmd].endswith('talk:'):
                    msg = msg + '%s *stuff* returns %s*stuff*\n' % (cmd, acmds[cmd])
            say(connection, nick, msg)
    except:
        connection.privmsg(channel, traceback.format_exc().splitlines()[-1])

def uespregextest(url2,url,connection,channel):
    print url
    print url2
    y=True
    code=httpget(url2)
    match = uespregex.findall(code)
    for pagename in match:
        url3 = 'http://www.uesp.net/wiki/%s' % pagename
        print url3
        if url3.lower() == url.lower():
            connection.privmsg(channel, url3)
            y=False
            break
    if url.lower().endswith('s') and y:
        url=url[:-1]
        url_temp=url2[:-1]
        code=httpget(url_temp)
        match = uespregex.findall(code)
        match = match[:-8]
        for pagename in match:
            url3 = 'http://www.uesp.net/wiki/%s' % pagename
            print url3
            if url3.lower() == url.lower():
                connection.privmsg(channel, url3)
                y=False
                break
    if y:
        connection.privmsg(channel, url2)
#>>> ";".join(["%s=%s" % (k, v) for k, v in params.items()])
#'server=mpilgrim;uid=sa;database=master;pwd=secret'


def enabled(server, channel, script):
    if server in disabled:
        if channel.lower() in disabled[server]:
            if script in disabled[server][channel.lower()]:
                 return False
            else:
                 enable =  True
        else:
            enable =  True
    else:
        enable = True
    if script in output_limit.keys() and enable:
        now = time.time()
        last_time = output_limit[script]['last_used']
        dtime=difs(now, last_time)
        if float(dtime) > output_limit[script]['limit']:
            enable = True
            output_limit[script]['last_used'] = now
        else: enable = False
    return enable

def onKick(connection,event):
    kicker = nicksplit(event.source())
    channel = event.target()
    kicked = event.arguments()[0]
    reason = event.arguments()[1]
    action='getting kicked from %s by %s for: %s' % (channel,kicker,reason)
    userlist[connection.server][channel.lower()].remove(kicked)
    if kicked.lower() in seen:
        seen[kicked.lower()]['secs']=time.time()
        seen[kicked.lower()]['action']=action
    else:
        seen[kicked.lower()]={'secs':time.time(),'action':action,'lines':0}
    action='kicking %s from %s for: %s' % (kicked,channel,reason)
    if kicker.lower() in seen:
        seen[kicker.lower()]['secs']=time.time()
        seen[kicker.lower()]['action']=action
    else:
        seen[kicker.lower()]={'secs':time.time(),'action':action,'lines':0}
    if kicked in adminlist:
        adminlist.remove(kicked)
    if kicked in sadminlist:
        sadminlist.remove(kicked)
    if kicked == connection.get_nickname():
        try:
            for num in (5.0,10.0,20.0,30.0): threading.Timer(num, connection.join, args=[channel]).start()
        except:
            pass

def httpget(url,data=None):
    """Returns a string that contains the source code of the url."""
    try:
        if data: data = urllib.urlencode(data)
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT) Peregrine/1.0' }
        request = urllib2.Request(url,data,headers)
        opener = urllib2.build_opener()
        f = opener.open(request)
        src = f.read(500000)
        f.close()
        return src
    except:
        pass

def onDisconnect(connection, event):
##    print event.source() #irc.nexuswar.com
##    print event.target() #nuthin'
##    print event.arguments() #['reason'] i.e. Connection reset by peer
    reason=event.arguments()[0]
    server=event.source()
    global sadminlist
    global adminlist
    sadminlist=[]
    adminlist=[]
    print 'Disconnected from ' + server + ' with "' + reason + '"!'


irc.add_global_handler('welcome', onWelcome)
irc.add_global_handler('pubmsg', onPubmsg)
irc.add_global_handler('pubmsg', UESP)
#irc.add_global_handler('pubmsg', dots)
irc.add_global_handler('privnotice', onPrivmsg)
irc.add_global_handler('privmsg', onPubmsg)
irc.add_global_handler('quit', onQuit)
irc.add_global_handler('part', onPart)
irc.add_global_handler('join', onJoin)
irc.add_global_handler("nick", nick)
irc.add_global_handler("kick", onKick)
irc.add_global_handler("all_raw_messages", raw)
irc.add_global_handler("namreply", names)
irc.add_global_handler("disconnect", onDisconnect)



def ping(server_object, server):
    try:
        server_object.ping(server)
    except:
        #server_object.disconnect() <-- don't need this because the failed ping calls onDisconnect!
        port = server_data[server]['port']
        nickname = server_data[server]['nickname']
        server_password = server_data[server]['password']
        server_object = irc.server()
        try:
            try:
                #3 try statements makes me feel dirty and kinky
                #not worse than anyhting else I do on this bot, though
                server_object.connect(server, port, nickname, ircname="Peregrine.  Owned by Atreus.", password = server_password)
            except:
                server_object.connect(server, port, nickname, password = server_password)
        except:
            print 'Unable to connect to %s (ping)' % server
            import traceback
            print traceback.format_exc()
    irc.execute_delayed(300, ping, (server_object, server))


for server in server_data:
    port = server_data[server]['port']
    nickname = server_data[server]['nickname']
    server_password = server_data[server]['password']
    server_object = irc.server()
    try:
        try:
            server_object.connect(server, port, nickname, ircname="Peregrine.  Owned by Atreus.", password = server_password)
        except:
            server_object.connect(server, port, nickname, password=server_password)
    except:
        print 'Unable to connect to %s' % server
    server_object.temp_timer = threading.Timer(300, ping, args=[server_object, server])
    server_object.temp_timer.start()





try:
    irc.process_forever()
except SystemExit:
    pass
except:
    import traceback
    print traceback.format_exc()
    raw_input()
