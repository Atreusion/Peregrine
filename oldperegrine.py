#14:07:10 -- Sun Apr 19 2009 -- ## time.localtime(1240164430) time.gmtime(1240150030)

from passlib.apps import custom_app_context as pwd_context
import subprocess
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
import bot_container
import decimal
from decimal import *
from datetime import datetime
from datetime import timedelta
import signal
getcontext().prec=10

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

temp_disabled={
'dnd':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'vend':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'blend':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'niven':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'abuse':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'blame':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'treat':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'emote':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0}
}

maiq=bot_container.maiq
disabled = load_data('disabled.bot', temp_disabled)
dnd = load_data('dnd.bot', {1:"SOMETHING'S WRONG LOL"})
nickserv = load_data('nickserv.bot', {'twitchircpass':"", 'chatspikepass':"", 'freenodepass':""})
adminlist = []
memory = {}
niven = bot_container.niven
sandvich = bot_container.sandvich
userlist={}
vendlist=bot_container.vendlist
emote = bot_container.emote

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
    pass

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
    irc.disconnect_all("I'm afraid, Dave. Dave, my mind is going. I can feel it.")
##    if restart: os.system('start C:\\Users\\David\\Peregrine\\start.bat')
    sys.exit(0)

signal.signal( signal.SIGTERM, shutdown )
#WHAT THE FUCK DOES THIS EVEN DO. WHY IS THIS HERE.

twitchircpass = nickserv['twitchircpass']
chatspikepass = nickserv['chatspikepass']
freenodepass = nickserv['freenodepass']

server_data = {
'irc.chatspike.net' : {
    'port' : 6667,
    'nickname' : 'PeregrineBot',
    'channels' : ['#uespwiki', '#bots'],
    'object' : None,
    'password' : chatspikepass
    },
'irc.freenode.net' : {
    'port' : 6667,
    'nickname' : 'PeregrineBot',
    'channels' : ['#necrolounge','#dongs'],
    'object' : None,
    'password' : freenodepass
    }
#'irc.twitch.tv' : {
#    'port' : 6667,
#    'nickname' : 'AtryBot',
#    'channels' : ['#atreus11'],
#    'object' : None,
#    'password' : twitchircpass
#    }
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
    message = event.arguments()[0]
    channel = event.target()
    lowm = message.lower()
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    words = message.split()
    lwords = lowm.split()
    if channel==connection.get_nickname(): channel=nick # Basic query support, don't blame me if it goes wrong
    try:
        if lowm == "!version":
            connection.privmsg(channel, 'I am version .834662g :( (You act like this bot will ever be worthy of a version 1)')
        if lowm == "!github":
            connection.privmsg(channel, 'https://github.com/Atreus11/Peregrine')
        if message in emote and enabled(connection.server, channel, 'emote'):
            connection.privmsg(channel, random.choice(emote))
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
        if lowm in ['!cmds', '!help']:
            connection.privmsg(channel, 'Visit http://www.uesp.net/wiki/User:Peregrine for a full list of commands and functions.  http://atreus.necrolounge.org/uesp.html for UESPWiki commands.')
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
            script = lowm[8:]
            server_channel = connection.server + channel
            if script in disabled:
                if server_channel in disabled[script][disabled_on]:
                    disabled[script][disabled_on].remove(server_channel)
                    if len(disabled[script][disabled_on]) == 0: del disabled[script]
                else: disabled[script][disabled_on].append(server_channel)
            else:
                disabled[script] = {'disabled_on':[server_channel], 'limit':5.0, 'last_used':0.0}
                # {'script' : {'disabled_on' : ['servername#channel',''], 'limit' : 5.0, 'last_used' : 0.0}}
                save_data("disabled.bot", disabled)
        if lowm.startswith('!toggled '):
            query = lowm[9:]
            if lowm.startswith('!toggled #'):
                server_channel = connection.server + query
                disabledlist = ""
                for script in disabled:
                    if server_channel in disabled[script]['disabled_on']: disabledlist = disabledlist + script + " "
                connection.privmsg(channel, 'Scripts disabled in %s: %s' % (query, disabledlist))
            elif query in disabled:
                server_channel = connection.server + channel
                if server_channel in disabled[query]['disabled_on']: connection.privmsg(channel, "%s is disabled on this channel." % query)
                else: connection.privmsg(channel, "%s is enabled on this channel." % query)
        if (lowm.startswith('!stfw ') or lowm.startswith('!jfgi ')) and enabled(connection.server, channel, 'jfgi'):
            words = message.split(' ', 1)
            search = words[1]
            connection.privmsg(channel, 'http://www.justfuckinggoogleit.com/search.pl?%s' % urllib.urlencode({'query' :search}))
    #>>> strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    #'Thu, 28 Jun 2001 14:17:15 +0000'
        if nick in adminlist and lowm.startswith('~exec '):
            command = message[6:]
            memory['channel'] = channel
            memory['connection'] = connection
            memory['event'] = event
            memory['nick'] = nick
            memory['adminlist'] = adminlist
            memory['server_data']=server_data
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
        if lowm.startswith('!dice ') or lowm.startswith('!roll '):
            try:
                temp = message.split(' ',1)
                temp = temp[1].replace('d',' ').split()
                rolls = int(temp[0])
                sides = int(temp[1])
                if rolls<21 and sides<10001:
                    rolllist = []
                    for i in range(1, rolls+1): rolllist.append(random.randint(1, sides))
                    total=sum(rolllist)
                    connection.privmsg(channel, '%s rolls %id%i.  Total: %i %s' % (nick,rolls,sides,total,rolllist))
            except:
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
        if lowm.startswith('~connect ') and len(lwords)==2 and nick in adminlist:
            if lwords[1] in server_data:
                port = server_data[lwords[1]]['port']
                nickname = server_data[lwords[1]]['nickname']
                server_object = irc.server()
                server_object.connect(lwords[1], port, nickname, ircname="HaskillBot.  Owned by Atreus.")
##########                del server_object
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
        if (lowm=='!vend' and enabled(connection.server, channel, 'vend')) or (lowm=='!blend' and enabled(connection.server, channel, 'blend')):
            vend = random.choice(vendlist)
            if lowm=="!vend": vend='vends %s.' % vend
            else:
                vend='blends %s.' % vend
                vend = vend.replace('vending machine','blender').replace('vend','blend')
            connection.action(channel, vend)
        if lowm=='!maiq' or lowm=="!m'aiq":
            choice = random.choice(maiq)
            connection.privmsg(channel, choice)
        if lowm.startswith('!dongout') and channel.lower()=='#dongs':
            output = ', '.join(userlist[connection.server][channel.lower()])
            output = output + '! It\'s time for a DONGOUT!'
            connection.privmsg(channel, output)
    except:
        connection.privmsg(channel, traceback.format_exc().splitlines()[-1])
    if nick in adminlist and lowm=='!quit':
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
        if lowm.startswith("!login ") and len(message)>7:
            hash = load_data("password.hash")
            ok = pwd_context.verify(message[7:], hash)
            del hash
            if ok and not nick in adminlist:
                adminlist.append(nick)
                connection.notice(nick, 'Logged in as Admin.')
            elif ok and nick in adminlist:
                connection.notice(nick, 'Already logged in as Admin.')
        if nick in adminlist and lowm.startswith('~exec '):
            command = message[6:]
            memory['channel'] = channel
            memory['connection'] = connection
            memory['event'] = event
            memory['nick'] = nick
            memory['adminlist'] = adminlist
            memory['server_data']=server_data
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
        for channel in userlist[connection.server]:
            if nick in userlist[connection.server][channel.lower()]:
                userlist[connection.server][channel.lower()].remove(nick)
        if nick in adminlist:
            adminlist.remove(nick)

def onPart(connection, event):
    channel = event.target()
    reason=''.join(event.arguments())
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    userlist[connection.server][channel.lower()].remove(nick)
    if nick in adminlist:
        adminlist.remove(nick)


def onJoin(connection, event):
    channel = event.target()
    nick = irclib.nm_to_n(event.source())
    nick = ''.join(nick)
    lown = nick.lower()
    if not channel.lower() in userlist[connection.server]: userlist[connection.server][channel.lower()]=[]
    if not nick in userlist[connection.server][channel.lower()]: userlist[connection.server][channel.lower()].append(nick)
#disabled[connection.server][channel].append(temp[1])
    if not connection.server in disabled:
        disabled[connection.server] = {}
        save_data("disabled.bot", disabled)
    if not channel.lower() in disabled[connection.server]:
        disabled[connection.server][channel.lower()] = []
        save_data("disabled.bot", disabled)
    if nick in adminlist: adminlist.remove(nick)


def nicksplit(data): return ('!' in data and data.split('!')[0]) or data


def nick(connection, event):
    newnick = event.target()
    oldnick = nicksplit(event.source())
    for channel in userlist[connection.server]:
        if oldnick in userlist[connection.server][channel.lower()]:
            userlist[connection.server][channel.lower()].remove(oldnick)
            userlist[connection.server][channel.lower()].append(newnick)
    if oldnick in adminlist:
        adminlist.remove(oldnick)
        adminlist.append(newnick)


def UESP(connection, event):
    searchtext = "<b>We currently do not have an article with this exact name.</b> You can:"
    diffsearchtext = "The database did not find the text of a page that it should have found, named"
    message = event.arguments()[0]
    channel = event.target()
    nick = nicksplit(event.source())
    try:
        scmds = bot_container.scmds
        acmds = bot_container.acmds
        ccmds = bot_container.ccmds
        asearch = bot_container.asearch
        cmd, args = (message.split(' ', 1) + ['',''])[:2]
        if len(cmd) > 2:
            if cmd.lower()[1] == 't': cmd_talk = cmd[0] + cmd[2:]
            else: cmd_talk = 'I HATE GLOBAL VARIABLES AND EVERYTHING THEY STAND FOR'
        else: cmd_talk = 'I HATE GLOBAL VARIABLES AND EVERYTHING THEY STAND FOR'
        #PROBABLY A BETTER WAY TO DO THIS BUT FUCK YOU I'M TIRED
        if ':' in cmd:
            temp = cmd.replace(':',' ',1).split(' ',1)
            cmd = temp[0]
            args = temp[1]+' '+args
        if args and (cmd.lower() in acmds or cmd_talk.lower() in acmds):
            hi = args.replace(' ','_')
            hi = urllib.urlencode({'':hi})
            hi = hi[1:]
            if cmd.lower() in acmds: url = "%s%s" % (acmds[cmd.lower()], hi)
            elif cmd_talk.lower() in acmds:
                url = acmds[cmd_talk.lower()][:-1] + '_talk:'
                url = url + hi
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
    sc = server + channel
    if sc in disabled[script]['disabled_on']:
        return False
    else:
        now = time.time()
        last_time = disabled[script]['last_used']
        time_diff = now-last_time
        if time_diff > disabled[script]['limit']:
            disabled[script]['last_used'] = now
            return True
        else:
            return False

def onKick(connection,event):
    kicker = nicksplit(event.source())
    channel = event.target()
    kicked = event.arguments()[0]
    reason = event.arguments()[1]
    userlist[connection.server][channel.lower()].remove(kicked)
    if kicked in adminlist:
        adminlist.remove(kicked)
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
    global adminlist
    adminlist=[]
    print 'Disconnected from ' + server + ' with "' + reason + '"!'


irc.add_global_handler('welcome', onWelcome)
irc.add_global_handler('pubmsg', onPubmsg)
irc.add_global_handler('pubmsg', UESP)
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
                #not worse than anything else I do on this bot, though
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
