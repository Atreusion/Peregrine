import os
import cPickle
import threading
import time
import random
import decimal
import traceback
from decimal import *


##class guessgameclass:
##    def __init__(self, connection, channel):
##        self.channel = channel
##        zeros = random.randint(1,9)
##        top = 10**zeros
##        seekrit=random.randint(0,top)
##        self.top = top
##        self.seekrit=seekrit
##        top=str(top)
##        connection.privmsg(self.channel, 'A new guessing game has started!  This number is between 0 and %s.' % top)
##    def guess(self, connection, channel, nick, guess):
##        if guess == self.seekrit:
##            connection.privmsg(channel, '%s just  guess the number!  It was %s.' % (nick, guess))
##            return 'win'
##        elif guess > self. seekrit:
##            connection.privmsg(channel, '%s: lower.' % nick)
##        else:
##            connection.privmsg(channel, '%s: higher.' % nick)

class RepeatingTimer:
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
        if self._timer: self._timer.stop()
    def run(self):
        try: self.function(*self.args, **self.kwargs)
        except: print traceback.format_exc()
        if self.repeat == -1:
            self.start()
        elif self.repeat > 0:
            self.repeat -= 1
            self.start()


def nicksplit(data): return ('!' in data and data.split('!')[0]) or data

def say(connection, channel, text):
    y = 0
    for line in text.splitlines():
        timer = threading.Timer(y, connection.privmsg, args=[channel, line])
        y += 1
        timer.start()

def difs(a,b,prec=None):
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


maiq = ["What does it mean to combine magic? Magic plus magic is still magic. M'aiq once tried to use two fire spells and burned his sweet roll!",
"Much snow in Skyrim. Enough snow. M'aiq does not want any more.",
"Skyrim was once the land of many butterflies. Now, not so much.",
"Snow falls. Why worry where it goes. M'aiq thinks the snowflakes are pretty.",
"M'aiq carries two weapons, to be safe. What if one breaks? That would be most unlucky.",
"M'aiq is always in search of calipers, yet finds none. Where could they have gone?",
"M'aiq hears many stories of war... yet few of them are true.",
"M'aiq has heard that the people of Skyrim are better looking than the ones in Cyrodiil. He has no opinion on the matter. All people are beautiful to him.",
"I saw a mudcrab the other day. Horrible creatures!",
"M'aiq does not understand what is so impressive about shouting. M'aiq can shout whenever he wants.",
"Why do soldiers bother with target practice? One learns best by hitting real people.",
"Something strange happens to Khajiit when they arrive in Skyrim.",
"Werebears? Where? Bears? Men that are bears?",
"Dragons were never gone. They were just invisible, and very very quiet.",
"M'aiq once climbed High Hrothgar. So many steps he lost count!",
"M'aiq does not remember his childhood, perhaps he never had one.",
"M'aiq is very practical. He has no need for mysticism.",
"Nords' armor has lots of fur. This sometimes makes M'aiq nervous.",
"Some like taking friends on adventures. M'aiq thinks being alone is better. Less arguing about splitting treasure.",
"Some say Alduin is Akatosh. Some say M'aiq is a Liar. Don't you believe either of those things.",
"It does not matter to M'aiq how strong or smart one is. It only matters what one can do.",
"M'aiq was soul trapped once. Not very pleasant. You should think about that once in a while.",
"Nords are so serious about beards. So many beards. M'aiq thinks they wish they had glorious manes like Khajiit.",
"M'aiq loves the people of Skyrim. Many interesting things they say to each other. ",
"M'aiq can travel fast across the land. Some lazy types take carriages. It is all the same to M'aiq.",
"Once M'aiq got in trouble in Riften, and fled to Windhelm. It is good that nobody there cared.",
"The people of Skyrim are more open-minded about certain things than people in other places.",
"M'aiq has heard it is dangerous to be your friend.",
"M'aiq knows why Falmer are blind. It has nothing to do with the Dwemer disappearing. Really.",
"M'aiq's father was also called M'aiq. As was M'aiq's father's father. At least, that's what his father said.",
"How does one know there was a city of Winterhold? M'aiq did not see it with his eyes, did you?",
"M'aiq knows much, tells some. M'aiq knows many things others do not.",
"M'aiq longs for a Colovian Fur Helm. Practical, yet stylish. M'aiq is very sad he does not have one.",
"M'aiq wishes he had a stick made out of fishies to give to you. Sadly, he does not.",
"M'aiq believes the children are our future. But he doesn't want them ruining all of our fun.",
"M'aiq thinks his people are beautiful. The Argonian people are beautiful as well. They look better than ever before.",
"Some people wish to throw their weapons. That seems foolish to M'aiq. If you hold your weapon, you only need one.",
"Some people want special bows that take too long to load and need special arrows called bolts. M'aiq thinks they are idiots.",
"Feet are for walking. Hands are for hitting. Or shaking. Or waving. Sometimes for clapping.",
"M'aiq prefers to adventure alone. Others just get in the way. And they talk, talk, talk.",
"People always enjoy a good fable. M'aiq has yet to find one, though. Perhaps one day.",
"So much easier to get around these days. Not like the old days. Too much walking. Of course, nothing stops M'aiq from walking when he wants.",
"M'aiq is glad he has a compass. Makes it easy to find things. Much better than wandering around like a fool.",
"Why would one want to swing a staff? A mace hurts more. Or a sword. Can't shoot a fireball from a sword, though.",
"I do not wish to fight on horseback. It is a good way to ruin a perfectly good horse... which is, to say, a perfectly good dinner.",
"Levitation is for fools. Why would we want to levitate? Once you are up high, there is nowhere to go but down.",
"It is good the people wear clothing. M'aiq wears clothing. Who would want to see M'aiq naked? Sick, sick people. Very sad.",
"I don't know why one would want to destroy a building. It takes time to make it. Much time.",
"I have seen dragons. Perhaps you will see a dragon. I won't say where I saw one. Perhaps I did not.",
"Werewolves? Where? Wolves? Men that are wolves? Many wolves. Everywhere. Many men. That is enough for M'aiq.",
"You wish to become a lich? It's very easy, my friend. Simply find the heart of a lich, combine it with the tongue of a dragon, and cook it with the flesh of a well-ridden horse. This combination is certain to make you undead.",
"Dragons? Oh, they're everywhere! You must fly very high to see most of them, though. The ones nearer the ground are very hard to see, being invisible.",
"M'Aiq sees lots of them in the ocean. M'Aiq knows you'll see one too if you swim far enough.",
"Horses.... Oh, M'Aiq loves horses! Especially with good cream sauce.",
"You would wish to ride upon a beast? There is a way... Go to one of the many silt-strider ports and pay your fee! You wish one for personal use? Bah! Walk if you must; run if you are chased!",
"Moving corpses? This sounds frightening to M'Aiq. The undead are nothing to be toyed with.",
"M'Aiq does not know this word. You wish others to help you in your quest? Coward! If you must, search for the Argonian Im-Leet, or perhaps the big Nord, Rolf the Uber. They will certainly wish to join you.",
"There is no mystery. M'Aiq knows all. The dwarves were here, and now they are not! They were very short folks... Or perhaps they were not. It all depends on your perspective. I'm sure they thought they were about the right height.",
"A horrible thing indeed. If you see one, let M'Aiq know. M'Aiq wants to make sure to look in the other direction.",
"Ahh... The beauty of the naked form. These Dunmer are rather prudish, are they not? Of course, there is an island you can reach filled with wonderful, naked, glistening bodies. It only appears when the moons are full, the rain falls, the seas run red, and it's M'Aiq's birthday.",
"Climbing ropes that hang is too difficult. M'Aiq prefers to climb the ones that are tied horizontally.",
"You seek the shrine that is no longer there? An interesting concept. Look to the seas to the West. There lies what was once the shrine. Take a deep breath and begin your search.",
"M'Aiq has heard of this. They've got all the money. Mudcrabs taking over everything. They already run Pelagiad.",
"I have only met one, but he was afraid of the water."]


scmds = {"!rc":"http://www.uesp.net/wiki/Special:Recentchanges", "!community portal":"http://www.uesp.net/wiki/UESPWiki:Community_Portal", "!cp":"http://www.uesp.net/wiki/UESPWiki:Community_Portal", "!admin noticeboard":"http://www.uesp.net/wiki/UESPWiki:Administrator_Noticeboard", "!an":"http://www.uesp.net/wiki/UESPWiki:Administrator_Noticeboard", "!rc":"http://www.uesp.net/wiki/Special:Recentchanges", "!fa":"http://www.uesp.net/wiki/UESPWiki:Featured_Articles"}
acmds = {'!sr':'http://www.uesp.net/wiki/Skyrim:','!skyrim':'http://www.uesp.net/wiki/Skyrim:',
'!template':'http://www.uesp.net/wiki/Template:',"!uesp":"http://www.uesp.net/wiki/",
"!uespwiki":"http://www.uesp.net/wiki/UESPWiki:", "!lore":"http://www.uesp.net/wiki/Lore:",
"!image":"http://www.uesp.net/wiki/Image:", "!morrowind":"http://www.uesp.net/wiki/Morrowind:",
"!mw":"http://www.uesp.net/wiki/Morrowind:", "!special":"http://www.uesp.net/wiki/Special:",
"!oblivion":"http://www.uesp.net/wiki/Oblivion:", "!ob":"http://www.uesp.net/wiki/Oblivion:",
"!triburnal":"http://www.uesp.net/wiki/Tribunal:", "!tr":"http://www.uesp.net/wiki/Tribunal:",
"!category":"http://www.uesp.net/wiki/Category:", "!cat":"http://www.uesp.net/wiki/Category:",
"!shivering":"http://www.uesp.net/wiki/Shivering:", "!si":"http://www.uesp.net/wiki/Shivering:",
"!user":"http://www.uesp.net/wiki/User:", "!arena":"http://www.uesp.net/wiki/Arena:",
"!ar":"http://www.uesp.net/wiki/Arena:", "!daggerfall":"http://www.uesp.net/wiki/Daggerfall:",
"!df":"http://www.uesp.net/wiki/Daggerfall:", "!battlespire":"http://www.uesp.net/wiki/Battlespire:",
"!bs":"http://www.uesp.net/wiki/Battlespire:", "!redguard":"http://www.uesp.net/wiki/Redguard:",
"!rg":"http://www.uesp.net/wiki/Redguard:", "!shadowkey":"http://www.uesp.net/wiki/Shadowkey:",
"!sk":"http://www.uesp.net/wiki/Shadowkey:", "!tob":"http://www.uesp.net/wiki/Oblivion_talk:",
"!tar":"http://www.uesp.net/wiki/Arena_talk:", "!tbs":"http://www.uesp.net/wiki/Battlespire_talk:",
"!tbm":"http://www.uesp.net/wiki/Bloodmoon_talk:", "!bm":"http://www.uesp.net/wiki/Bloodmoon:",
"!tcat":"http://www.uesp.net/wiki/Category_talk:", "!tdf":"http://www.uesp.net/wiki/Daggerfall_talk:",
"!tgen":"http://www.uesp.net/wiki/General_talk:", "!thelp":"http://www.uesp.net/wiki/Help_talk:",
"!tim":"http://www.uesp.net/wiki/Image_talk:", "!tlore":"http://www.uesp.net/wiki/Lore_talk:",
"!tmdw":"http://www.uesp.net/wiki/Mediawiki_talk:", "!tmw":"http://www.uesp.net/wiki/Morrowind_talk:",
"!trg":"http://www.uesp.net/wiki/Redguard_talk:", "!tsi":"http://www.uesp.net/wiki/Shivering_talk:",
"!ttemp":"http://www.uesp.net/wiki/Template_talk:", "!tt3m":"http://www.uesp.net/wiki/Tes3Mod_talk:",
"!tt4m":"http://www.uesp.net/wiki/Tes4Mod_talk:", "!ttr":"http://www.uesp.net/wiki/Tribunal_talk:",
"!tuesp":"http://www.uesp.net/wiki/UESPWiki_talk:", "!tuser":"http://www.uesp.net/wiki/User_talk:",
"!tsr":"http://www.uesp.net/wiki/Skyrim_talk:", "!dragonborn":"http://www.uesp.net/wiki/Dragonborn:",
"!db":"http://www.uesp.net/wiki/Dragonborn:", "!online":"http://www.uesp.net/wiki/Online:",
"!on":"http://www.uesp.net/wiki/Online:"}
ccmds = {'!ctemplate':'http://www.uesp.net/w/index.php?title=Template:', "!cuesp":"http://www.uesp.net/w/index.php?title=",
"!cuespwiki":"http://www.uesp.net/w/index.php?title=UESPWiki:", "!clore":"http://www.uesp.net/w/index.php?title=Lore:",
"!cimage":"http://www.uesp.net/w/index.php?title=Image:", "!cmorrowind":"http://www.uesp.net/w/index.php?title=Morrowind:",
"!cmw":"http://www.uesp.net/w/index.php?title=Morrowind:", "!ccuser":"http://www.uesp.net/w/index.php?title=Special:Contributions/",
"!coblivion":"http://www.uesp.net/w/index.php?title=Oblivion:", "!cob":"http://www.uesp.net/w/index.php?title=Oblivion:",
"!ctriburnal":"http://www.uesp.net/w/index.php?title=Tribunal:", "!ctr":"http://www.uesp.net/w/index.php?title=Tribunal:",
"!ccategory":"http://www.uesp.net/w/index.php?title=Category:", "!ccat":"http://www.uesp.net/w/index.php?title=Category:",
"!cshivering":"http://www.uesp.net/w/index.php?title=Shivering:", "!csi":"http://www.uesp.net/w/index.php?title=Shivering:",
"!cuser":"http://www.uesp.net/w/index.php?title=User:", "!carena":"http://www.uesp.net/w/index.php?title=Arena:",
"!car":"http://www.uesp.net/w/index.php?title=Arena:", "!cdaggerfall":"http://www.uesp.net/w/index.php?title=Daggerfall:",
"!cdf":"http://www.uesp.net/w/index.php?title=Daggerfall:", "!cbattlespire":"http://www.uesp.net/w/index.php?title=Battlespire:",
"!cbs":"http://www.uesp.net/w/index.php?title=Battlespire:", "!credguard":"http://www.uesp.net/w/index.php?title=Redguard:",
"!crg":"http://www.uesp.net/w/index.php?title=Redguard:", "!cshadowkey":"http://www.uesp.net/w/index.php?title=Shadowkey:",
"!csk":"http://www.uesp.net/w/index.php?title=Shadowkey:", "!ctob":"http://www.uesp.net/w/index.php?title=Oblivion_talk:",
"!ctar":"http://www.uesp.net/w/index.php?title=Arena_talk:", "!ctbs":"http://www.uesp.net/w/index.php?title=Battlespire_talk:",
"!ctbm":"http://www.uesp.net/w/index.php?title=Bloodmoon_talk:", "!cbm":"http://www.uesp.net/w/index.php?title=Bloodmoon:",
"!ctcat":"http://www.uesp.net/w/index.php?title=Category_talk:", "!ctdf":"http://www.uesp.net/w/index.php?title=Daggerfall_talk:",
"!ctgen":"http://www.uesp.net/w/index.php?title=General_talk:", "!cthelp":"http://www.uesp.net/w/index.php?title=Help_talk:",
"!ctim":"http://www.uesp.net/w/index.php?title=Image_talk:", "!ctlore":"http://www.uesp.net/w/index.php?title=Lore_talk:",
"!ctmdw":"http://www.uesp.net/w/index.php?title=Mediawiki_talk:", "!ctmw":"http://www.uesp.net/w/index.php?title=Morrowind_talk:",
"!ctrg":"http://www.uesp.net/w/index.php?title=Redguard_talk:", "!ctsi":"http://www.uesp.net/w/index.php?title=Shivering_talk:",
"!cttemp":"http://www.uesp.net/w/index.php?title=Template_talk:", "!ctt3m":"http://www.uesp.net/w/index.php?title=Tes3Mod_talk:",
"!ctt4m":"http://www.uesp.net/w/index.php?title=Tes4Mod_talk:", "!cttr":"http://www.uesp.net/w/index.php?title=Tribunal_talk:",
"!ctuesp":"http://www.uesp.net/w/index.php?title=UESPWiki_talk:", "!ctuser":"http://www.uesp.net/w/index.php?title=User_talk:",
"!csr":"http://www.uesp.net/w/index.php?title=Skyrim:", "!ctsr":"http://www.uesp.net/w/index.php?title=Skyrim_talk:"}
asearch = {'!ob':'&ns116=1','!si':'&ns126=1','!uesp':'&ns0=1','!uespwiki':'&ns4=1','!lore':'&ns130=1','!mw':'&ns110=1','!tr':'&ns112=1','!bm':'&ns114=1'}
niven={'1a':'Never throw shit at an armed man.',
'1b':'Never stand next to someone who is throwing shit at an armed man.',
'2':'Never fire a laser at a mirror.',
'3':"Mother Nature doesn't care if you're having fun.",
'4':'Giving up freedom for security has begun to look naive.  F x S = k.',
'5':"Psi and/or magical powers, if real, are nearly useless.",
'6':"It is easier to destroy than create.",
'7':"Any damn fool can predict the past.",
'8':"History never repeats itself.",
'9':"Ethics change with technology.",
'10':"Anarchy is the least stable of social structures.",
'11':"There is a time and place for tact.",
'12':"The ways of being human are bounded but infinite.",
'13':"When your life starts to look like a soap opera, it's time to change the channel.",
'14a':"The only universal message in science fiction: There exist minds that think as well as you do, but differently.",
'14b':"The gene-tampered turkey you're talking to isn't necessarily one of them.",
'15':"Fuzzy Pink Niven's Law: Never waste calories.",
'16':"There is no cause so right that one cannot find a fool following it.",
'17':"No technique works if it isn't used.",
'18':"Not responsible for advice not taken.",
'19':"Think before you make the coward's choice. Old age is not for sissies.",
'20':"Never let a waiter escape."}
sandvich=["Ahh, so filling! Hahaha!",
"Moist and delicious! Hehaha!",
"Sandvich make me strong!",
"I am full of sandvich, and I am coming for you!",
"Sandvich and I are coming for you!",
"Don't run! It's just ham!",
"Baloney is perfect fuel for killing tiny cowards!",
"Saww-ndvich, sandwich!",
"Me and my... sandwich.",
'What was that sandvich? "Kill them all"? Good idea! Hahaha!',
"Look at you tiny-itty-bitty men running from sandvich!",
"You are a loose cannon sandvich, but you are a damn good cop!",
"Sandvich and me going to beat your ass!",
"Kill them all! Hahaha!",
"Run from the sandwich!",
"Baloney! Hahahaha!",
"That vas delicious!"]
wordroulette1=[-2500,-1000,-500,-250,-100,-100,-100,-100,-100,-50,-50,-50,-50,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-10,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,5,5,5,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,10,10,10,13,20,20,20,20,20,20,25,25,25,25,25,25,25,25,25,42,50,50,50,50,50,50,100,100,100,100,100,100,100,100,100,100,250,250,250,314,500,666,777,1000,1337,5000]
wordroulette2=[-10,-5,-2.5,-2.5,-2.5,-2.5,-2,-2,-2,-2,-2,-2,-1,-1,-1,-1,-1,-1,-1,-.5,-.5,-.5,-.5,-.5,-.5,-.5,-.5,-.1,-.1,-.1,-.1,-.1,-.1,0,0,0,0,0,0,0,0,0,0,.1,.1,.1,.5,.5,.5,.5,.5,.5,.5,.5,.5,.5,.75,.75,.75,.75,.75,.75,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.337,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2.5,2.5,2.5,2.5,3.14,4.2,5,5,6.66,10]