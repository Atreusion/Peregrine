# 19:37:58 Thursday, May 12, 2016
import pydle
import sys
import bot_container
import random
import time
import pickle
import os
import threading
import traceback

# {'script' : {'disabled_on' : ['servername#channel',''], 'limit' : 5.0, 'last_used' : 0.0}}
# Have a local file, load it on startup, save whenever changed
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

server_data = {
'irc.chatspike.net' : {
    'port' : 6697,
    'nickname' : 'Peregrine3',
    'channels' : ['#peregrine3'],
    'server_password' : None,
    'ns_password' : None,
    'tls' : True
    },
'irc.freenode.net' : {
    'port' : 6697,
    'nickname' : 'Peregrine3',
    'channels' : ['#peregrine3'],
    'server_password' : None,
    'ns_password' : None,
    'tls' : True
    }
#'irc.twitch.tv' : {
#    'port' : 6667,
#    'nickname' : 'AtryBot',
#    'channels' : ['#atreus11'],
#    'password' : None
#    }
}

disabled = load_data('disabled.bot')

class MyClient(pydle.Client):
    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        for channel in server_data[self.connection.hostname]['channels']:
            self.join(channel)

    def on_join(self, channel, user):
        super().on_join(channel, user)
#        msg = 'Hey there, %s!' % user
#        self.message(channel, msg)

    @pydle.coroutine
    def on_message(self, channel, user, message):
        super().on_message(channel, user, message)
        try:
            low_message = message.lower()
            if low_message.startswith('!test'):
                self.message(channel, "%s, this is a test in %s on %s." % (user, channel, self.connection.hostname))
            if message == "!die":
                for client in pool.clients:
                    self.disconnect(client)
                sys.exit(0)
            if low_message == "!github":
                self.message(channel, "https://github.com/Atreusion/Peregrine/")
            if message in bot_container.emote and enabled(self.connection.hostname, channel, 'emote'):
                self.message(channel, random.choice(bot_container.emote))
            if message == "!randomname":
                userchoice = random.choice(list(self.users.keys()))
                userchoice = self.users[userchoice]['nickname']
                self.message(channel, userchoice)
        except SystemExit:
            pass
        except:
            print(traceback.format_exc())
    def on_raw(self, message):
        super().on_raw(message)
        print(message)

# Setup pool and connect clients.
pool = pydle.ClientPool()
for server in server_data:
    client = MyClient(server_data[server]['nickname'])
    pool.connect(client, server, tls=server_data[server]['tls'], password=server_data[server]['server_password'])
# Handle all clients in the pool at once.
try:
    pool.handle_forever()
except SystemExit:
    pass
except:
    print(traceback.format_exc())
    input()
