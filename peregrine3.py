#14:07:10 -- Sun Apr 19 2009 -- ## time.localtime(1240164430) time.gmtime(1240150030)

import irc.client
from passlib.apps import custom_app_context as pwd_context
import subprocess
import sys
import threading
import traceback
import random
import pickle
import re
import datetime
import time
from time import strftime
from time import gmtime
import os
import urllib.parse
import bot_container
from datetime import datetime
from datetime import timedelta


irc_object = irc.client.Reactor()

def shutdown():
#    checktimer.stop()
    irc_object.disconnect_all("I'm afraid, Dave. Dave, my mind is going. I can feel it.")
    sys.exit(0)
	
def load_data( filename, default={}, override=True ):
    """some_list = load_data('some_list.bot', ['default', 'list'])"""
    path = os.sep.join([os.getcwd(), 'files', filename])
    if os.path.exists(path):
        f = open(path, 'rb')
        try:
            data = pickle.load(f)
            f.close()
            return data
        except EOFError:
            if override: return default
    return default

def save_data( filename, data ):
    """save_data("some_list.bot", some_list)"""
    path = os.sep.join([os.getcwd(), 'files', filename])
    with open( path, 'wb' ) as f: pickle.dump(data, f)
    
class RepeatingTimer:
    """Given to Atreus by Kindari.  I think he made it.  Example commented out below."""
    #def test(): print 'test'
    #timer = RepeatingTimer(5, test, repeat=10) // 5 being the seconds between each command, and 10 being the repeats.  if -1 is repeat, infinite repeat
    #timer.start()
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
        except: print(traceback.format_exc())
        if self.repeat == -1:
            self.start()
        elif self.repeat > 0:
            self.repeat -= 1
            self.start()

def remove_dups(L):
    """Removes duplicate items from list L in place."""
    # Work backwards from the end of the list.
    for i in range(len(L)-1, -1, -1):
        # Check to see if the current item exists elsewhere in
        # the list, and if it does, delete it.
        if L[i] in L[:i]:
            del L[i]
			
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

def httpget(url,data=None):
    """Returns a string that contains the source code of the url."""
    try:
        if data: data = urllib.parse.urlencode(data)
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT) Peregrine/1.0' }
        request = urllib.Request(url,data,headers)
        opener = urllib.build_opener()
        f = opener.open(request)
        src = f.read(500000)
        f.close()
        return src
    except:
        pass
		
def enabled(server, channel, script):
    """Checks to see if script is disabled on server's channel."""
    sc = server + channel
    if script not in disabled: return True
    elif sc in disabled[script]['disabled_on']: return False
    else:
        now = time.time()
        last_time = disabled[script]['last_used']
        time_diff = now-last_time
        if time_diff > disabled[script]['limit']:
            disabled[script]['last_used'] = now
            return True
        else:
            return False
            
maiq=bot_container.maiq
adminlist = []
memory = {}
niven = bot_container.niven
sandvich = bot_container.sandvich
userlist={}
vendlist=bot_container.vendlist
emote = bot_container.emote
temp_disabled={
'dnd':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'vend':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'blend':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'niven':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'abuse':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'blame':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'treat':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'emote':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0},
'objection':{'disabled_on' : [], 'limit':5.0, 'last_used':0.0}
}
disabled = load_data('disabled.bot', temp_disabled)
dnd = load_data('dnd.bot', {1:"SOMETHING'S WRONG LOL"})
nickserv = load_data('nickserv.bot', {'twitchircpass':"", 'chatspikepass':"", 'freenodepass':""})
twitchircpass = nickserv['twitchircpass']
chatspikepass = nickserv['chatspikepass']
freenodepass = nickserv['freenodepass']
server_data = {
'irc.chatspike.net' : {
    'port' : 6667,
    'nickname' : 'PeregrineBot',
    'channels' : ['#bots'],#['#uespwiki', '#bots', '#pandemonium'],
    'object' : None,
    'password' : chatspikepass
    }
#'irc.freenode.net' : {
#    'port' : 6667,
#    'nickname' : 'PeregrineBot',
#    'channels' : ['#necrolounge','#dongs'],
#    'object' : None,
#    'password' : freenodepass
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
    message = event.arguments[0]
    channel = event.target
    lowm = message.lower()
    nick = event.source.split('!')[0]
    words = message.split()
    lwords = lowm.split()
    if channel==connection.get_nickname(): channel=nick # Basic query support, don't blame me if it goes wrong
    try:
        if lowm == "!version":
            connection.privmsg(channel, 'I am version .834662g :( (You act like this bot will ever be worthy of a version 1)')
        if lowm.startswith("~status ") and len(message)>8 and nick in adminlist:
            service = message[8:]
            try:
                output = subprocess.check_output(['service', service, 'status'])
                status = output.splitlines()[2].decode('utf-8')[11:27]
                connection.privmsg(channel, service + " " + status)
            except subprocess.CalledProcessError:
                errtrace = traceback.format_exc()
                if errtrace[-9:-1] == "status 3":
                    connection.privmsg(channel, service + " not active")
            except:
                pass
        if lowm == "!github":
            connection.privmsg(channel, 'https://github.com/Atreus11/Peregrine')
        if message in emote and enabled(connection.server, channel, 'emote'):
            connection.privmsg(channel, random.choice(emote))
        if lowm.startswith("!wp "):
            args = message[4:]
            args=urllib.parse.urlencode({'' :args})
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
            url = 'http://www.google.com/search?%s' % urllib.parse.urlencode({'q' :search})
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
            secs = int(time.time()) - 1240150030
            d = timedelta(seconds=secs)
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
                if server_channel in disabled[script]['disabled_on']:
                    disabled[script]['disabled_on'].remove(server_channel)
                    if len(disabled[script]['disabled_on']) == 0: del disabled[script]
                    connection.privmsg(channel, "%s was enabled on %s." % (script, channel))
                    save_data("disabled.bot", disabled)
                else:
                    disabled[script]['disabled_on'].append(server_channel)
                    connection.privmsg(channel, "%s was disabled on %s." % (script, channel))
                    save_data("disabled.bot", disabled)
            else:
                disabled[script] = {'disabled_on':[server_channel], 'limit':5.0, 'last_used':0.0}
                connection.privmsg(channel, "%s was disabled on %s." % (script, channel))
                # {'script' : {'disabled_on' : ['servername#channel',''], 'limit' : 5.0, 'last_used' : 0.0}}
                save_data("disabled.bot", disabled)
        if lowm.startswith('!toggled '):
            query = lowm[9:]
            if lowm.startswith('!toggled #'):
                server_channel = connection.server + query
                disabledlist = ""
                for script in disabled:
                    if server_channel in disabled[script]['disabled_on']: disabledlist = disabledlist + script + " "
                if not disabledlist == '': connection.privmsg(channel, 'Scripts disabled in %s: %s' % (query, disabledlist))
            elif query in disabled:
                server_channel = connection.server + channel
                if server_channel in disabled[query]['disabled_on']: connection.privmsg(channel, "%s is disabled on this channel." % query)
                else: connection.privmsg(channel, "%s is enabled on this channel." % query)
        if (lowm.startswith('!stfw ') or lowm.startswith('!jfgi ')) and enabled(connection.server, channel, 'jfgi'):
            words = message.split(' ', 1)
            search = words[1]
            connection.privmsg(channel, 'http://www.justfuckinggoogleit.com/search.pl?%s' % urllib.parse.urlencode({'query' :search}))
    #>>> strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    #'Thu, 28 Jun 2001 14:17:15 +0000'
        if nick in adminlist and lowm.startswith('~exec '):
            command = message[6:]
            memory['channel'] = channel
            memory['connection'] = connection
            memory['event'] = event
            memory['nick'] = nick
            memory['server_data']=server_data
            memory['adminlist'] = adminlist
            memory['disabled'] = disabled
            memory['userlist']=userlist
            if command.startswith('say '):
                stuff=command[4:]
                command='connection.privmsg(channel, %s)' % stuff
                try:
                    exec(command, memory)
                except:
                    stuff=stuff.replace('"','\"')
                    command='connection.privmsg(channel, "%s")' % stuff
                    exec(command, memory)
            else:
                exec(command, memory)
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
                if lwords[1] in list(niven):
                    connection.privmsg(channel, '%s: %s' % (lwords[1], niven[lwords[1]]))
                else:
                    n = random.choice(list(niven))
                    connection.privmsg(channel, '%s: %s' % (n, niven[n]))
            else:
                n = random.choice(list(niven))
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
                                elif search in rule[1].lower() and iteration != number:
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
                    print('SOMETHING WENT WRONG, OH SO WRONG BABY')
            else:
                n = random.choice(list(dnd))
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
    if nick in adminlist and lowm=='~quit':
        shutdown()
        
def nick_strip(s):
    if s[0] in '!+%@&~:': return s[1:]
    return s
		
def names(connection, event):
    channel = event.arguments[1].lower()
    nicks = event.arguments[2].split()
    nicks = [nick_strip(nick) for nick in nicks]
    if not connection.server in userlist: userlist[connection.server] = {}
    if not channel in userlist[connection.server]: userlist[connection.server][channel] = []
    userlist[connection.server][channel].extend(nicks)
    remove_dups(userlist[connection.server][channel])

def raw(connection, event):
    args = ''.join(event.arguments).split()
    timenow = time.strftime('%X', time.localtime())
    if len(args)>2:
        if args[1] == 'PRIVMSG' and not args[2].lower() == connection.nickname.lower():
            nick = args[0].split("!")[0]
            print('%s %s %s <%s> %s' % (connection.server, timenow, args[2], nick, ' '.join(args[3:])[1:]))
        else:
            arguments = 'ERROR'.join(event.arguments)
            print(connection.server + ' ' + timenow + ' ' + arguments)
    elif args[0]=='PING':
        pass
    else:
        print(connection.server + ' ' + timenow + ' ' + 'ERROR'.join(event.arguments))

def onPrivmsg(connection, event):
    message = event.arguments[0]
    channel = event.target
    lowm = message.lower()
    try:
        nick = event.source.split('!')[0]
    except:
        nick = 'Atreus'
        connection.notice(nick,'something went wrong, onprivmsg')
        print(traceback.format_exc())
    try:
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
            memory['disabled'] = disabled
            if command.startswith('say '):
                stuff=command[4:]
                command='connection.privmsg(nick, %s)' % stuff
                try:
                    exec(command, memory)
                except:
                    stuff=stuff.replace('"','\"')
                    command='connection.privmsg(nick, "%s")' % stuff
                    exec(command, memory)
            else:
                exec(command, memory)
        command = lowm.split(' ', 1)
    except:
        connection.privmsg(nick, traceback.format_exc().splitlines()[-1])
		

def onQuit(connection, event):
    reason=''.join(event.arguments)
    nick = event.source.split('!')[0]
    if not nick == connection.get_nickname():
        for channel in userlist[connection.server]:
            if nick in userlist[connection.server][channel.lower()]:
                userlist[connection.server][channel.lower()].remove(nick)
        if nick in adminlist:
            adminlist.remove(nick)

def onPart(connection, event):
    channel = event.target
    reason=''.join(event.arguments)
    nick = event.source.split('!')[0]
    userlist[connection.server][channel.lower()].remove(nick)
    if nick in adminlist:
        adminlist.remove(nick)

def onJoin(connection, event):
    channel = event.target
    nick = event.source.split('!')[0]
    lown = nick.lower()
    if not channel.lower() in userlist[connection.server]: userlist[connection.server][channel.lower()]=[]
    if not nick in userlist[connection.server][channel.lower()]: userlist[connection.server][channel.lower()].append(nick)
    if nick in adminlist: adminlist.remove(nick)
	
def nick(connection, event):
    newnick = event.target
    oldnick = event.source.split('!')[0]
    for channel in userlist[connection.server]:
        if oldnick in userlist[connection.server][channel.lower()]:
            userlist[connection.server][channel.lower()].remove(oldnick)
            userlist[connection.server][channel.lower()].append(newnick)
    if oldnick in adminlist:
        adminlist.remove(oldnick)
        adminlist.append(newnick)
		
def onKick(connection,event):
    kicker = event.source.split('!')[0]
    channel = event.target
    kicked = event.arguments[0]
    reason = event.arguments[1]
    userlist[connection.server][channel.lower()].remove(kicked)
    if kicked in adminlist:
        adminlist.remove(kicked)
    if kicked == connection.get_nickname():
        global adminlist
        adminlist = []
        try:
            for num in (5.0,10.0,20.0,30.0): threading.Timer(num, connection.join, args=[channel]).start()
        except:
            pass
			
def onDisconnect(connection, event):
##    print event.source() #irc.nexuswar.com
##    print event.target() #nuthin'
##    print event.arguments() #['reason'] i.e. Connection reset by peer
    reason=event.arguments[0]
    server=event.source
    global adminlist
    adminlist=[]
    print('Disconnected from ' + server + ' with "' + reason + '"!')
	
def ping(server_object, server):
    try:
        server_object.ping(server)
    except:
        port = server_data[server]['port']
        nickname = server_data[server]['nickname']
        server_password = server_data[server]['password']
        server_object = irc_object.server()
        try:
            try:
                #3 try statements makes me feel dirty and kinky
                #not worse than anything else I do on this bot, though
                server_object.connect(server, port, nickname, ircname="Peregrine.  Owned by Atreus.", password = server_password)
            except:
                server_object.connect(server, port, nickname, password = server_password)
        except:
            print('Unable to connect to %s (ping)' % server)
            import traceback
            print(traceback.format_exc())
#    irc.execute_delayed(300, ping, (server_object, server))
#Do I need this line?
	
irc_object.add_global_handler('welcome', onWelcome)
irc_object.add_global_handler('pubmsg', onPubmsg)
#irc_object.add_global_handler('pubmsg', UESP)
irc_object.add_global_handler('privnotice', onPrivmsg)
irc_object.add_global_handler('privmsg', onPubmsg)
irc_object.add_global_handler('quit', onQuit)
irc_object.add_global_handler('part', onPart)
irc_object.add_global_handler('join', onJoin)
irc_object.add_global_handler("nick", nick)
irc_object.add_global_handler("kick", onKick)
irc_object.add_global_handler("all_raw_messages", raw)
irc_object.add_global_handler("namreply", names)
irc_object.add_global_handler("disconnect", onDisconnect)

for server in server_data:
    port = server_data[server]['port']
    nickname = server_data[server]['nickname']
    server_password = server_data[server]['password']
    server_object = irc_object.server()
	#def connect(self, server, port, nickname, password=None, username=None, ircname=None, connect_factory=connection.Factory()):
    try:
        try:
            server_object.connect(server, port, nickname, ircname="Peregrine.  Owned by Atreus.", password = server_password)
        except:
            server_object.connect(server, port, nickname, password=server_password)
    except:
        print('Unable to connect to %s' % server)
    server_object.temp_timer = threading.Timer(300, ping, args=[server_object, server])
    server_object.temp_timer.start()

try:
    irc_object.process_forever()
except SystemExit:
    sys.exit(0)
except:
    import traceback
    print(traceback.format_exc())
    input()
