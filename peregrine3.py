# 19:37:58 Thursday, May 12, 2016
import pydle

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
            exit()
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
    import traceback
    print(traceback.format_exc())
    input()
