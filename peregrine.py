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
hparser = HParser()
os.system('title Peregrine')
getcontext().prec=10

#Use with the form: mylist=truerandom.getnum(min,max,amount)
#mylist will be a list containing the true random numbers.
#def foo(): for i in range(5): return i # returns 0

server_data = {
'irc.nexuswar.com' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#stagecrew', '#necrolounge'],
    'object' : None
    }, # note the comma
'irc.chatspike.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#uespwiki', '#bots', '#trspam', '#equilibrium', '#Aetherius', '#internet'],
    'object' : None
    },
'staticfree.foonetic.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#boats'],
    'object' : None
    },
'irc.deviantart.com' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#devart'],
    'object' : None
    },
'napier.subluminal.net' : {
    'port' : 6667,
    'nickname' : 'Peregrine',
    'channels' : ['#bots', '#boats'],
    'object' : None
    },
'verne.freenode.net' : {
    'port' : 6667,
    'nickname' : 'HaskillBot',
    'channels' : ['#necrolounge'],
    'object' : None
    }
}

irc = irclib.IRC()

def load_data( path, default={}):
    if os.path.exists(path):
        f = open(path, 'r')
        data = cPickle.load(f)
        f.close()
        return data
    return default

def save_data( path, data )
    with open( path, 'w' ) as f: cPickle.dump(data, f)

disabled = load_data('C:\\Users\\David\\Peregrine\\files\\disabled.bot')
dnd = load_data('C:\\Users\\David\\Peregrine\\files\\dnd.bot', {1:'SOMETHING\'S WRONG LOL'})
nickserv = load_data('C:\\Users\\David\\Peregrine\\files\\nickserv.bot')

adminlist = []
sadminlist = []
memory = {}
niven = stuffz.niven
sandvich = stuffz.sandvich
userlist={}
#dnd=stuffz.dnd
sdw = re.compile("<a href=\"http://en\.wikipedia\.org/wiki/.*\">(.*)</a>")
uespregex = re.compile("<a href=\"/wiki/(.*)\" title=")
titlefind = re.compile("<title\s?>(.*)<\/title\s?>", re.I)

tfw = load_data('C:\\Users\\David\\Peregrine\\files\\tfw.bot')
seen = load_data('C:\\Users\\David\\Peregrine\\files\\seen.bot')



class RepeatingTimer:
    """Given to Atreus by Kindari.  I think he made it."""
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
    tfwo = load_data('C:\\Users\\David\\Peregrine\\files\\tfw.bot')
    if not tfwo == tfw:
        save_data("C:\\Users\\David\\Peregrine\\files\\tfw.bot", tfw)
        
    seeno = load_data('C:\\Users\\David\\Peregrine\\files\\seen.bot')
    if not seeno == seen:
        save_data("C:\\Users\\David\\Peregrine\\files\\seen.bot", seen)




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



def pquit(restart=False):
    checktimer.stop()
    if os.path.exists('C:\\Users\\David\\Peregrine\\files\\tfw.bot'):
        with open('C:\\Users\\David\\Peregrine\\files\\tfw.bot', 'r') as f: tfwo = cPickle.load(f)
    else:
        tfwo = {}
    if not tfwo == tfw:
        f=open("C:\\Users\\David\\Peregrine\\files\\tfw.bot", "w")
        cPickle.dump(tfw, f)
        f.close()
        del f
    if os.path.exists('C:\\Users\\David\\Peregrine\\files\\seen.bot'):
        with open('C:\\Users\\David\\Peregrine\\files\\seen.bot', 'r') as f: seeno = cPickle.load(f)
    else:
        seeno = {}
    if not seeno == seen:
        f=open("C:\\Users\\David\\Peregrine\\files\\seen.bot", "w")
        cPickle.dump(seen, f)
        f.close()
        del f
    irc.disconnect_all("I'm afraid, Dave. Dave, my mind is going. I can feel it.")
    if restart: os.system('start C:\\Users\\David\\Peregrine\\start.bat')
    sys.exit(0)


class twitter_class:
    def __init__(self):
        if os.path.exists('C:\\Users\\David\\Peregrine\\files\\twitter.bot'):
            with open('C:\\Users\\David\\Peregrine\\files\\twitter.bot', 'r') as f: self.login = cPickle.load(f)
            f.close()
            del f
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
    if channel==connection.get_nickname(): channel=nick
    try:
        action='speaking in %s' % channel
        if nick.lower() in seen:
            seen[nick.lower()]['secs']=time.time()
            seen[nick.lower()]['action']=action
            if 'lines' in seen[nick.lower()]: seen[nick.lower()]['lines']+=1
            else: seen[nick.lower()]['lines']=1
            if 'chars' in seen[nick.lower()]: seen[nick.lower()]['chars']+=len(message)
            else: seen[nick.lower()]['chars']=len(message)
##            if 'lols' in seen[nick.lower()]: seen[nick.lower()]['lols']+=message.lower().count('lol')
##            else: seen[nick.lower()]['lols']=message.lower().count('lol')
        else:
            seen[nick.lower()]={'secs':time.time(),'action':action,'lines':1,'chars':len(message)}#,'lols':message.lower().count('lol')}
        if lowm == "!version":
            connection.privmsg(channel, 'I am version .82g :( (You act like this bot will ever be worthy of a version 1)')
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
        if lowm == "!boondock" and enabled(connection.server, channel, 'boondock'):
            connection.privmsg(channel, 'And shepherds we shall be, for Thee, my Lord, for Thee.  Power hath descended forth from Thy hand, that our feet may swiftly carry out Thy command.  So we shall flow a river forth to Thee, and teeming with souls shall it ever be,  In Nomine Patris, Et Fili, Et Spiritus Sancti.')
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
        if nick in sadminlist and lowm=='!movielist':
            if os.path.exists('C:\\Users\\David\\Peregrine\\files\\movies.bot'):
                f = open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "r")
                mlist = cPickle.load(f)
                f.close()
                del f
                total='Movies: %s' % ', '.join(mlist)
                if len(total)>200:
                    total='%s%s%s' % (total[:199],'\n',total[200:])
                if len(total)>402:
                    total='%s%s%s ... continued' % (total[:401],'\n',total[402:])
                say(connection, channel, total)
            else:
                connection.privmsg(channel, 'No movies in the list.')
        if 'bot' in lowm and 'give' in lowm and 'a movie' in lowm:
            if os.path.exists('C:\\Users\\David\\Peregrine\\files\\movies.bot'):
                f = open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "r")
                mlist = cPickle.load(f)
                f.close()
                del f
                connection.privmsg(channel, random.choice(mlist))
            else:
                connection.privmsg(channel, 'No movies in the list.')
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
        if nick in sadminlist and lowm.startswith('!addmovie '):
            if os.path.exists('C:\\Users\\David\\Peregrine\\files\\movies.bot'):
                f = open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "r")
                mlist = cPickle.load(f)
                f.close()
                del f
            else:
                mlist = []
            words = lowm.split(' ', 1)
            mov = words[1]
            mov = ''.join(mov)
            if mov in mlist:
                connection.privmsg(channel, '"%s" is already in Des and Atry\'s movie list.' % (mov, ))
            else:
                mlist.append(mov)
                f=open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "w")
                cPickle.dump(mlist, f)
                f.close()
                del f
                connection.privmsg(channel, '"%s" added to Des and Atry\'s movie list.' % (mov, ))
        if nick in adminlist and lowm.startswith('!delmovie '):
            if os.path.exists('C:\\Users\\David\\Peregrine\\files\\movies.bot'):
                f = open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "r")
                mlist = cPickle.load(f)
                f.close()
                del f
            else:
                mlist = []
            words = lowm.split(' ', 1)
            mov = words[1]
            mov = ''.join(mov)
            if not mov in mlist:
                connection.privmsg(channel, '"%s" is not in Des and Atry\'s movie list.' % (mov, ))
            else:
                mlist.remove(mov)
                f=open("C:\\Users\\David\\Peregrine\\files\\movies.bot", "w")
                cPickle.dump(mlist, f)
                f.close()
                del f
                connection.privmsg(channel, '"%s" removed from Des and Atry\'s movie list.' % (mov, ))
        if lowm.startswith('~toggle ') and nick in adminlist:
    #disabled[server][channel]
            if len(words) == 2:
                if words[1] in disabled[connection.server][channel.lower()]:
                    disabled[connection.server][channel.lower()].remove(words[1])
                    connection.privmsg(channel, "%s is enabled." % words[1])
                else:
                    disabled[connection.server][channel.lower()].append(words[1])
                    connection.privmsg(channel, "%s is disabled." % words[1])
                f = open('C:\\Users\\David\\Peregrine\\files\\disabled.bot','w')
                cPickle.dump(disabled,f)
                f.close()
                del f
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
        #131246 <@Maid> You can use all alphanumeric, `, |, _, [, ]
        #131253 <@Maid> Also ^, yeah
        #131256 <&Atreus> k.
        #131309 <@Maid> I think you can use {}<> too, but don't recall
        #131314 * Maid is now known as {}
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
                    url = 'http://www.thefuckingweather.com/?zipcode=%s' % area
                    units = 'DEGREES FAHRENHEIT'
                else:
                    url = 'http://www.thefuckingweather.com/?zipcode=%s&CELSIUS=yes' % area
                code = httpget(url)
                weather = code.split('<div id="content"><div class="large" >',1)[1].split('</div>',1)[0].split('<br />')
                degrees = weather[0][:-7]
                if letter=='k':
                    degrees=str(float(degrees)+273.15)
                    units = 'KELVIN'
                elif letter=='c': units='DEGREES CELSIUS'
                comment = '. '.join(weather[2:])
                comments = code.split('<span>')[1].split('</span>')[0]
                dtime=difs(time.time(),a)
                connection.privmsg(channel, '%s: %s %s?!  %s.  %s (%s second%s)' % (temp, degrees, units, comment, comments, dtime, ((dtime <> '1.00' and 's') or '')))
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
                connection.privmsg(channel, 'Error')
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
        if lowm.startswith('!content') and len(message)==9:
            url='http://content%s.uesp.net/server-status' % message[8]
#            try:
            code=httpget(url)
            uptime=code.split('Server uptime: ')[1].split('<br>')[0]
            accesses=code.split('Total accesses: ')[1].split(' - ')[0]
            traffic=code.split('Total Traffic: ')[1].split('<br>')[0]
            rs=code.split('CPU load<br>\n')[1].split('<br>')[0]
            servers=code.split('B/request<br>\n\n')[1].split('\n')[0]
            load=code.split('CPU load<br>')[0].split()[-1]
            connection.privmsg(channel, 'Uptime: %s.  Load: %s CPU.  Accesses: %s.  Traffic: %s.  Bandwidth: %s.  Servers: %s' % (uptime,load,accesses,traffic,rs,servers))
            del code
        if lowm.startswith('~aquit') and nick in sadminlist:
            for each in server_data.values(): each['object'].quit((len(words)>1 and message[7:]) or 'Peregrine shutting down.')
            print "'%s' used by %s" % (message,nick)
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
        if lowm.startswith('!treat ') and len(lwords)>1:
            treated=' '.join(words[1:])
            if treated.lower() == connection.get_nickname().lower():
                connection.action(channel, 'wags his tail.')
            else:
                connection.action(channel, 'gives a treat to ' + treated)
##        if lowm.startswith('!oldest ') and len(lwords)==2:
##            if lwords[1].isdigit():
##                num=int(lwords[1])
##                if num<21:
##                    d={}
##                    for name in seen:
##                        d[seen[name].values()[1]]=name
##                    sseen=sorted(d)[:num]
##                    cmd=''
##                    for timex in sseen:
##                        cmd=cmd+d[timex]+', '
##                    cmd=cmd[:-2]
##                    connection.privmsg(channel, '%s are the oldest people seen.' % cmd)
##                    del d
##                    del sseen
        if lowm.startswith('~delseen ') and len(lwords)>1 and nick in adminlist:
            del seen[lowm[9:]]
            connection.privmsg(channel, '%s deleted from seen.' % lowm[9:])
        if lowm.startswith('!stats ') and len(words)>2:
##            if lwords[1]=='lols' and lwords[2] in seen:
##                lols=str(seen[lwords[2]]['lols'])
##                lines=seen[lwords[2]]['lines']
##                lolpercentage=str(float(lols)/float(lines)*100.0)[:5]
##                connection.privmsg(channel, '%s has said "lol" %s times, about %s%% percent of their lines contain it.' % (lwords[2],lols,lolpercentage))
            if lwords[1]=='lines' and lwords[2] in seen:
                connection.privmsg(channel, '%s has spoken %s lines.' % (lwords[2],seen[lwords[2]]['lines']))
            if (lwords[1]=='characters' or lwords[1]=='chars' or lwords[1]=='letters') and lwords[2] in seen:
                chars=str(seen[lwords[2]]['chars'])
                lines=seen[lwords[2]]['lines']
                charaverage=str(float(chars)/float(lines))[:5]
                connection.privmsg(channel, '%s has typed %s characters, resulting in a %s average per line.' % (lwords[2],chars,charaverage))
        if nick in sadminlist and lowm.startswith('~dellines'):
            n1 = len(seen)
            for name in seen.keys():
                if seen[name]['lines']<11:
                    del seen[name]
            n2 = len(seen)
            diff=difs(n1,n2)
            connection.privmsg(channel, '%s names cleared.' % diff)
        if nick in sadminlist and lowm.startswith('~delchars'):
            n1 = len(seen)
            for name in seen.keys():
                if seen[name]['chars']<21:
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
                    if message[4] in ['[','{',"'",'"','(','<'] and lwords[0][-1] in [']','}',"'",'"',')','>'] and lwords[0][5:-1].isdigit(): number=int(lwords[0][5:-1])
                    else: number=1
                    iteration=1
                    items=dnd.items()
                    items.sort()
                    for rule in items:
                        if search in rule[1].lower() and iteration==number:
                            connection.privmsg(channel, str(rule[0]) + ': ' + rule[1])
                            break
                        elif search in rule[1].lower() and iteration<>number:
                            number-=1
                else:
                    n = random.choice(dnd.keys())
                    connection.privmsg(channel, '%s: %s' % (n, dnd[n]))
                    print 'derpderpderp\n%s' % message
            else:
                n = random.choice(dnd.keys())
                connection.privmsg(channel, '%s: %s' % (n, dnd[n]))
        if lowm.startswith('!tweet ') and channel.lower()=='#necrolounge':
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
        if lowm=='!vend':
            vend=httpget('https://itvends.com/vend.php')
            vend='vends %s.' % vend
            connection.action(channel, vend)
##        if lowm=='!dfterm' and nick in sadminlist:
##            os.system('"C:\Program Files\dfterm2\dfterm2.exe" --create-appdir')
##        if lowm.startswith('!lm ') and len(words)>2:
##            reciever = lwords[1]
##            messager = nick
##            message_time = strftime("%d %b %Y %H:%M:%S GMT", gmtime())
##            if reciever in messages:messages[receiver]=[{'t':message_time, 'from':messager, 'message':' '.join(words[2:]]
##            else: messages[receiver]=[{'t':message_time, 'from':messager, 'message':' '.join(words[2:]]
##            connection.privmsg(channel, 'Message saved.')
##        if lowm=='!gm' and nick.lower() in messages:
##            messagestring=''
##            for message_unf in messages[nick.lower()]:
##                message_f = 'From <%s> on %s: %s' % (messages[nick.lower()]['from'], messages[nick.lower()]['t'], messages[nick.lower()][message])
##                messagestring = message_f + '\n'
##            say(connection, channel, messagestring)
    except:
        if channel.lower()<>'#uespwiki':
            tits = '\n'.join(traceback.format_exc().splitlines())
#        connection.privmsg(channel, traceback.format_exc().splitlines()[-1])
            say(connection, channel, tits)
        else:
            connection.privmsg(channel, traceback.format_exc().splitlines()[-1])
    if nick in sadminlist and lowm=='!quit':
        pquit()
    if nick in sadminlist and lowm=='!restart':
        pquit(restart=True)

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


##def difd(e,s):
##        t=str(e-s)
##        t=t.replace('.',':').split(':')
##        hours=int(t[0])
##        minutes=int(t[1])
##        secs=t[2]
##        days=0
##        while hours>=24:
##            days+=1
##            hours-=24
##        if days==0: d=''
##        elif days==1: d=' %s day, ' % str(days)
##        else: d=' %s days, ' % str(days)
##        if hours==0: h=''
##        elif hours==1: h=' %s hour, ' % str(hours)
##        else: h=' %s hours, ' % str(hours)
##        if minutes==0: m=''
##        elif minutes==1: m=' %s minute, ' % str(minutes)
##        else: m=' %s minutes, ' % str(minutes)
##        l=[d,h,m,secs]
##        return l


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
        dots = ['Dark`Star quickly unzips his pants.', 'Rick Astley shifts uncomfortably.',
        'You suddenly realize it is unnaturally quiet.', 'Desdemona ogles disconcertingly.', 'You quickly discover one of you has an erection.',
        'You hear the muffled yells of a Mac user being ignored.', 'You hear the shrill screams of an emo kid getting the sense beat into them.',
        'You suddenly realize TylerRilm is nekkid.', "Save your breath $who, you'll need it to blow up your date.", "I am $who's colon.  I get cancer.  I kill $who.",
        'Everybody points and laughs at $who.', "You enjoy the sweet smell of $who's hopes and dreams burning.", "$who and $someone, sitting in a tree...",
        'Peregrine quickly looks up.', 'Peregrine quickly pulls his pants up.', 'Peregrine stares at the wall.', 'Peregrine runs into the nearest wall.']
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
    #Bucket!bucket@irc.peeron.com PRIVMSG #bucket :Something.001832 <&Atreus> ~exec say event.arguments()
##001832 <&Atreus> ~exec say event.arguments()
##001833 <&Peregrine> ['~exec say event.arguments()']
##001843 <&Atreus> ~exec say event.source()
##001844 <&Peregrine> Atreus!Erasmus@nw-55A3C2E8.bltmmd.fios.verizon.net
##001851 <&Atreus> ~exec say event.target()
##001851 <&Peregrine> #stagecrew
##001857 <&Atreus> ~exec say event.eventtype()
##001857 <&Peregrine> pubmsg
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
##            s = arguments.split()
##            if s[1]=="353" and s[3]=="=":
##                nicks = s[5:]
##                nicks = [nick_strip(nick) for nick in nicks]
##                if not connection.server in userlist: userlist[connection.server]={}
##                userlist[connection.server][s[4]]=nicks
##            del s

def onPrivmsg(connection, event):
    message = event.arguments()[0]
    channel = event.target()
    lowm = message.lower()
    try:
        nick = irclib.nm_to_n(event.source())
        nick = ''.join(nick)
    except:
        nick = 'Atreus'
        connection.notice(nick,'something went wrong')
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


##def onq(connection, event):
##    message = event.arguments()[0]
##    channel = event.target()
##    lowm = message.lower()
##    nick = irclib.nm_to_n(event.source())
##    nick = ''.join(nick)
##    try:
###        print '<Query> %s: %s: %s' % (connection.server, nick, message)
##        if nick in sadminlist and lowm.startswith('~exec '):
##            command = message[6:]
##            memory['channel'] = channel
##            memory['connection'] = connection
##            memory['event'] = event
##            memory['nick'] = nick
##            memory['sadminlist'] = sadminlist
##            memory['adminlist'] = adminlist
##            memory['server_data']=server_data
##            memory['seen']=seen
##            memory['tfw']=tfw
##            if command.startswith('say '):
##                stuff=command[4:]
##                command='connection.privmsg(nick, %s)' % stuff
##                try:
##                    exec command in memory
##                except:
##                    stuff=stuff.replace('"','\"')
##                    command='connection.privmsg(nick, "%s")' % stuff
##                    exec command in memory
##            else:
##                exec command in memory
##    except:
##        connection.privmsg(nick, traceback.format_exc().splitlines()[-1])

def onQuit(connection, event):
    reason=''.join(event.arguments())
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    if reason: action='quitting with: %s' % (reason)
    else: action='quitting'
    for channel in userlist[connection.server]:
        if nick in userlist[connection.server][channel.lower()]:
            userlist[connection.server][channel.lower()].remove(nick)
    if nick.lower() in seen:
        seen[nick.lower()]['secs']=time.time()
        seen[nick.lower()]['action']=action
    else:
        seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
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
        seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
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
        seen[nick.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
    if (event.source().endswith('.bltmmd.east.verizon.net') or event.source().endswith('.mibbit.com') or event.source().endswith('.balt.east.verizon.net')) and nick.startswith('Desde'):
        connection.privmsg(channel, 'Atreus!  Guess who\'s on!')
#disabled[connection.server][channel].append(temp[1])
    if not connection.server in disabled:
        disabled[connection.server] = {}
        f = open('C:\\Users\\David\\Peregrine\\files\\disabled.bot','w')
        cPickle.dump(disabled,f)
        f.close()
        del f
    if not channel.lower() in disabled[connection.server]:
        disabled[connection.server][channel.lower()] = []
        f = open('C:\\Users\\David\\Peregrine\\files\\disabled.bot','w')
        cPickle.dump(disabled,f)
        f.close()
        del f
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
        seen[newnick.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
    action='changing nick to ' + newnick
    if oldnick.lower() in seen:
        seen[oldnick.lower()]['secs']=time.time()
        seen[oldnick.lower()]['action']=action
    else:
        seen[oldnick.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
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
#        tits = '\n'.join(traceback.format_exc().splitlines())
        connection.privmsg(channel, traceback.format_exc().splitlines()[-1])
#        say(connection, channel, tits)

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
        url2=url2[:-1]
        code=httpget(url2)
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
                 return True
        else:
            return True
    else:
        return True

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
        seen[kicked.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
    action='kicking %s from %s for: %s' % (kicked,channel,reason)
    if kicker.lower() in seen:
        seen[kicker.lower()]['secs']=time.time()
        seen[kicker.lower()]['action']=action
    else:
        seen[kicker.lower()]={'secs':time.time(),'action':action,'lines':0,'chars':0}#,'lols':0}
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
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
        request = urllib2.Request(url,data,headers)
        opener = urllib2.build_opener()
        f = opener.open(request)
        src = f.read(500000)
        f.close()
        return src
    except:
        pass


irc.add_global_handler('welcome', onWelcome)
irc.add_global_handler('pubmsg', onPubmsg)
irc.add_global_handler('pubmsg', UESP)
irc.add_global_handler('pubmsg', dots)
irc.add_global_handler('privnotice', onPrivmsg)
irc.add_global_handler('privmsg', onPubmsg)
##irc.add_global_handler('privmsg', onq)
irc.add_global_handler('quit', onQuit)
irc.add_global_handler('part', onPart)
irc.add_global_handler('join', onJoin)
irc.add_global_handler("nick", nick)
irc.add_global_handler("kick", onKick)
irc.add_global_handler("all_raw_messages", raw)
irc.add_global_handler("namreply", names)
##irc.add_global_handler("disconnect", onDisconnect)
#irc.add_global_handler('privmsg',unogame.mainf)
#    "250": "luserconns",
#    "251": "luserclient",
#    "252": "luserop",
#    "253": "luserunknown",
#    "254": "luserchannels",
#    "255": "luserme",

for server in server_data:
    port = server_data[server]['port']
    nickname = server_data[server]['nickname']
    server_object = irc.server()
    try:
        try:
            server_object.connect(server, port, nickname, ircname="Peregrine.  Owned by Atreus.")
        except:
            server_object.connect(server, port, nickname)
    except:
        print 'Unable to connect to %s' % server




try:
    irc.process_forever()
except SystemExit:
    pass
except:
    import traceback
    print traceback.format_exc()
    raw_input()