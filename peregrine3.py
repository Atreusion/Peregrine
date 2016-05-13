# 19:37:58 Thursday, May 12, 2016
import pydle
import sys
import bot_container
import random
import time

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

class MyClient(pydle.Client):
    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        for channel in server_data[self.connection.hostname]['channels']:
            self.join(channel)

    def on_join(self, channel, user):
        super().on_join(channel, user)
        msg = 'Hey there, %s!' % user
        self.message(channel, msg)

    @pydle.coroutine
    def on_message(self, channel, user, message):
        super().on_message(channel, user, message)
        low_message = message.lower()
        if low_message.startswith('!test'):
            self.message(channel, "%s, this is a test in %s on %s." % (user, channel, self.connection.hostname))
        if low_message == "!die":
            print("IT WORKS I GUESS")
            for client in pool:
                self.disconnect(client)
            sys.exit(0)
        if low_message == "!github":
            self.message(channel, "https://github.com/Atreusion/Peregrine/")
#        if message in bot_container.emote and enabled(self.connection.hostname, channel, 'emote'):
#            self.message(channel, random.choice(bot_container.emote))
    def on_raw(self, message):
        super().on_raw(message)
        print(message)

# Want to combine output_limit and disabled.  Have it be:
# {'script' : {'disabled_on' : ['servername#channel',''], 'limit' : blah}}
# Have a local file, load it on startup, save whenever changed
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
    import traceback
    print(traceback.format_exc())
    input()
