import pydle

class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """
    
    def on_raw(self, message):
        print(message)

    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        self.join('#peregrine')

    def on_join(self, channel, user):
        super().on_join(channel, user)
        self.message(channel, 'Hey there, {user}!', user=user)
    
    @pydle.coroutine
    def on_message(self, target, source, message):
        super().on_message(target, source, message)
        if message == "!disconnect":
            self.disconnect()
        

# Setup pool and connect clients.
pool = pydle.ClientPool()
servers = ['irc.chatspike.net',]

for server in servers:
    client = pydle.MyClient('Peregrine3', realname = "testbot")
    pool.connect(client, server, 6697, tls=True)

# Handle all clients in the pool at once.
pool.handle_forever()
