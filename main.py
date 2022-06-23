import discord
from discord.ext import commands
import datetime
from config import *
from discord.utils import get
from discord_components import *
from discord_slash import SlashCommand
from discord import Embed
import time
import os
#from replit import db
#from database import *
import asyncio
import random

carryCost = int(5)
stone = int(5)
plank = int(10)
canny = int(15)
twine = int(20)
illegal = ["/help", "/msk", "/carryldb", "/host", "/hostldb", "/helpedldb", "/ldb", "/leeches", "/cancel", "/blackjack",
           "/highorlow", "/highscore", "/potofluck", "/mali", "/topmali", "/roulette"]
# db[745277161228861461] = [745277161228861461, 69405, 0, 3, 0, 0, 10, 0] #cdog
# db[538394329333497865] = [538394329333497865, 892005, 1, 0, 0, 0, 1, 0] #king
# db[712957215308251146] = [712957215308251146, 34000, 2, 0, 3, 1, 0, 0] #lucar
#db[925764075915472967] = [925764075915472967, 54320, 0, 0, 0, 0, 0, 0]  # cnub
#del db['925764075915472967']
# del db["Lucaro#2705"]
# del db["KingMalivore#5150"]


bot = commands.Bot(command_prefix="/", description='Test bot for discord.py')
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Bot is online")
    DiscordComponents(bot)


@slash.slash(name="prices", description="Lists claim prices")
async def prices(ctx):
    prices = discord.Embed(title="CARRY PRICES", color=0xDFFF00)
    prices.add_field(name="Twine Peaks", value=twine, inline=True)
    prices.add_field(name="Canny Valley", value=canny, inline=True)
    prices.add_field(name="Plankerton", value=plank, inline=True)
    prices.add_field(name="Stonewood", value=stone, inline=True)
    prices.add_field(name="MSK", value=carryCost, inline=True)
    prices.timestamp = datetime.datetime.now()
    await ctx.send(embed=prices)


@slash.slash(name="msk", description="Request an msk carry")
async def msk(ctx):
    name = ctx.author
    userid = ctx.author.id
    hostName = ctx.author.name
    hostAvatar = ctx.author.avatar_url
    botChannel = 976418819532808192

    def checkUser(author, userid):
        ids = []
        for key in db.keys():
            ids.append(db[key][0])
        if userid in ids:
            pass
        else:
            db[userid] = [userid, 20, 0, 0, 0, 0]

    checkUser(name, userid)

    def ticketUpdate(userid, tickets):
        ids = []
        emblems = []
        for key in db.keys():
            ids.append(db[key][0])
            emblems.append(db[key][1])
        num = emblems[ids.index(userid)]
        if num + tickets >= 0:
            return True
        else:
            return False

    if ctx.channel.id == botChannel:
        if ticketUpdate(userid, -1 * (carryCost)) is True:

            def check(author, channel):
                def inner_check(message):
                    return message.author == author and channel == botChannel

                return inner_check

            await ctx.channel.send('Epic? or type /cancel to cancel')
            epicName = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
            if epicName.content in illegal:
                epicName = int(epicName.content)
            await ctx.channel.send('Power level? or type /cancel to cancel')
            power = False
            powerLvl = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
            while not power:
                try:
                    powerLvl = int(powerLvl.content)
                    power = True
                except ValueError:
                    if powerLvl.content in illegal:
                        powerLvl = int(powerLvl.content)
                    else:
                        await ctx.channel.send("Enter an integer only")
                        powerLvl = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
            msk = get(ctx.channel.guild.roles, name='msk_pings')
            location = bot.get_channel(941418365229092894)
            await location.send(f"{msk.mention}")
            mskHost = discord.Embed(title=f"{hostName}\'s storm king help", color=0xDFFF00)
            mskHost.set_thumbnail(url=hostAvatar)
            mskHost.add_field(name="Epic Username", value=epicName.content, inline=True)
            mskHost.add_field(name="Power Level", value=powerLvl, inline=True)
            mskHost.add_field(name="Helper", value="Required", inline=True)

            mskHost.timestamp = datetime.datetime.now()
            claim = Button(style=ButtonStyle.green, label="Claim")
            unclaim = Button(style=ButtonStyle.red, label="Unclaim")
            end = Button(style=ButtonStyle.grey, label="End")
            cancel = Button(style=ButtonStyle.grey, label="Cancel")
            msg = await location.send(embed=mskHost, components=[[claim, end, cancel]])
            spots = 1

            def check(res):
                return res.channel == location and msg == res.message

            def ticketChange(userid, tickets):
                for key in db.keys():
                    if db[key][0] == userid:
                        db[key][1] += tickets

            while True:
                res = await bot.wait_for("button_click", check=check)
                user = res.component.label
                if user == "Claim":
                    claimerID = res.user.id
                    if claimerID != userid:
                        mskHost = discord.Embed(title=f"{hostName}\'s storm king help", color=0xDFFF00)
                        mskHost.set_thumbnail(url=hostAvatar)
                        mskHost.add_field(name="Epic Username", value=epicName.content, inline=True)
                        mskHost.add_field(name="Power Level", value=powerLvl, inline=True)
                        mskHost.add_field(name="Helper", value=f"<@{claimerID}>", inline=True)

                        await msg.edit(embed=mskHost, components=[[unclaim, end, cancel]])
                        checkUser(name, userid)
                        checkUser(res.user, claimerID)
                        correct = ticketChange(userid, -1 * carryCost)
                        correct = ticketChange(claimerID, carryCost)
                        happy = await ctx.author.guild.fetch_member(userid)
                        await happy.send(f"{res.user.name} is requesting to carry you")
                        spots = 0
                    else:
                        await res.respond(content="You cannot claim your own request!")

                elif user == "Unclaim":
                    unclaimerid = res.user.id
                    if unclaimerid == claimerID:
                        mskHost = discord.Embed(title=f"{hostName}\'s storm king help", color=0xDFFF00)
                        mskHost.set_thumbnail(url=hostAvatar)
                        mskHost.add_field(name="Epic Username", value=epicName.content, inline=True)
                        mskHost.add_field(name="Power Level", value=powerLvl, inline=True)
                        mskHost.add_field(name="Helper", value="Required", inline=True)

                        await msg.edit(embed=mskHost, components=[[claim, end, cancel]])

                        checkUser(name, userid)
                        checkUser(res.user, unclaimerid)
                        correct = ticketChange(userid, carryCost)
                        correct = ticketChange(unclaimerid, -1 * carryCost)
                        sad = await ctx.author.guild.fetch_member(userid)
                        await sad.send(f"{res.user.name} is no longer wanting to carry you")
                        spots = 1
                    else:
                        await res.respond(content="You have not claimed this carry!")

                elif user == "End":
                    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
                    endid = res.user.id
                    if endid == userid or role in res.user.roles:
                        mskHost = discord.Embed(title=f"{hostName}\'s storm king success", color=0xDFFF00)
                        mskHost.set_author(name=hostName, icon_url=hostAvatar)
                        mskHost.add_field(name=f"{hostName} appreciates the help", value="#1 Victory Royale",
                                          inline=False)

                        await msg.edit(embed=mskHost, components=[])
                        if spots == 0:
                            for key in db.keys():
                                if db[key][0] == claimerID:
                                    db[key][2] += 1
                                elif db[key][0] == endid:
                                    db[key][3] += 1
                                else:
                                    pass
                        else:
                            pass
                    else:
                        await res.respond(content="This is not your request to end!")
                elif user == "Cancel":
                    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
                    endid = res.user.id
                    if endid == userid or role in res.user.roles:
                        mskHost = discord.Embed(title=f"{hostName} cancelled their request", color=0xDFFF00)
                        mskHost.set_author(name=hostName, icon_url=hostAvatar)

                        await msg.edit(embed=mskHost, components=[])
                        checkUser(name, userid)
                        checkUser(res.user, endid)
                        if spots == 0:
                            correct = ticketChange(claimerID, -1 * carryCost)
                            correct = ticketChange(userid, carryCost)
                            lonely = await ctx.author.guild.fetch_member(claimerID)
                            await lonely.send(f"{hostName} cancelled their request. You received no emblems")
                        else:
                            pass
                    else:
                        await res.respond(content="This is not your request to cancel!")
                await res.respond(type=6)


        else:
            await ctx.send(content=f"<@{userid}> not enough emblems")
    else:
        botChannelName = bot.get_channel("botChannel")
        await ctx.send(content=f"<@{userid}> please use "f"<#{botChannel}>")


@slash.slash(name="blackjack", description="Play blackjack")
async def blackjack(ctx):
    name = ctx.author
    userid = ctx.author.id
    hostName = ctx.author.name
    hostAvatar = ctx.author.avatar_url
    botChannel = 976418865141669928
    channel = bot.get_channel(botChannel)
    cards = [["Spades", "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
             ["Hearts", "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
             ["Diamonds", "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
             ["Clubs", "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]]

    player = []
    playersuit = []
    pVal = []
    dealer = []
    dealersuit = []
    dVal = []

    def checkCount(playerCards, count):
        if 11 in playerCards:
            if count > 21:
                count -= 10
        return count

    def checkUser(author, userid):
        ids = []
        for key in db.keys():
            ids.append(db[key][0])
        if userid in ids:
            pass
        else:
            db[userid] = [userid, 20, 0, 0, 0, 0, 0]

    checkUser(name, userid)

    def getEmblems():
        for key in db.keys():
            if db[key][0] == userid:
                return db[key][1]

    emblems = getEmblems()
    count = "Your Emblems: " + str(emblems)

    def ticketChange(userid, bet):
        for key in db.keys():
            if db[key][0] == userid:
                db[key][1] += bet

    main = discord.Embed(title="Welcome to Blackjack", color=0xDFFF00)
    main.set_thumbnail(url=hostAvatar)
    main.add_field(name="Please place your bet", value=count, inline=True)
    main.timestamp = datetime.datetime.now()
    ten = Button(style=ButtonStyle.green, label=10)
    twenty = Button(style=ButtonStyle.green, label=20)
    fifty = Button(style=ButtonStyle.green, label=50)
    hundred = Button(style=ButtonStyle.green, label=100)
    if emblems >= 10 and emblems < 20:
        blackjack = await ctx.send(embed=main, components=[[ten]])
    elif emblems >= 20 and emblems < 50:
        blackjack = await ctx.send(embed=main, components=[[ten, twenty]])
    elif emblems >= 50 and emblems < 100:
        blackjack = await ctx.send(embed=main, components=[[ten, twenty, fifty]])
    elif emblems >= 100:
        blackjack = await ctx.send(embed=main, components=[[ten, twenty, fifty, hundred]])
    else:
        await ctx.send("You do not have enough Emblems to play")

    def check(res):
        return res.channel.id == botChannel and blackjack == res.message

    while True:
        res = await bot.wait_for("button_click", check=check)
        user = res.component.label
        if res.user.id == userid:
            if user == str(10):
                bet = 10
                ember = getEmblems()
                if ember - bet < 0:
                    boggle = await channel.fetch_message(res.message.id)
                    await boggle.delete()
                    boggle = int("bhjcd")
                else:
                    ticketChange(userid, -bet)
            elif user == str(20):
                bet = 20
                ember = getEmblems()
                if ember - bet < 0:
                    boggle = await channel.fetch_message(res.message.id)
                    await boggle.delete()
                    boggle = int("bhjcd")
                else:
                    ticketChange(userid, -bet)
            elif user == str(50):
                bet = 50
                ember = getEmblems()
                if ember - bet < 0:
                    boggle = await channel.fetch_message(res.message.id)
                    await boggle.delete()
                    boggle = int("bhjcd")
                else:
                    ticketChange(userid, -bet)
            elif user == str(100):
                bet = 100
                ember = getEmblems()
                if ember - bet < 0:
                    boggle = await channel.fetch_message(res.message.id)
                    await boggle.delete()
                    boggle = int("bhjcd")
                else:
                    ticketChange(userid, -bet)

            else:
                pass
            await res.respond(type=6)
            for i in range(0, 2):
                suit = random.randint(0, 3)
                num = random.randint(1, len(cards[suit]) - 1)
                chosen = cards[suit][num]
                del (cards[suit][num])
                player.append(chosen)
                playersuit.append(cards[suit][0])

            for i in range(0, 2):
                suit = random.randint(0, 3)
                num = random.randint(1, len(cards[suit]) - 1)
                chosen = cards[suit][num]
                del (cards[suit][num])
                dealer.append(chosen)
                dealersuit.append(cards[suit][0])

            try:
                total = int(player[0] + player[1])
            except:
                try:
                    total = int(player[0])
                except:
                    try:
                        total = int(player[1])
                    except:
                        total = 10

            def cardValue(val, count):
                if count == "A":
                    if total + 11 > 21:
                        val.append(1)
                        return int(1)
                    else:
                        val.append(11)
                        return int(11)
                elif count == "J":
                    val.append(10)
                    return int(10)
                elif count == "Q":
                    val.append(10)
                    return int(10)
                elif count == "K":
                    val.append(10)
                    return int(10)
                else:
                    val.append(count)
                    return count

            count1 = cardValue(pVal, player[0])
            total = count1
            count2 = cardValue(pVal, player[1])

            spade = discord.utils.get(bot.emojis, name='spades')
            heart = discord.utils.get(bot.emojis, name='hearts')
            diamond = discord.utils.get(bot.emojis, name='diamonds')
            club = discord.utils.get(bot.emojis, name='clubs')
            q = discord.utils.get(bot.emojis, name='grey_question')

            if count1 + count2 != 21:
                pCards = "Your Cards: \n"
                dCards = "Dealers Cards: \n"
                total = count1 + count2
                # for i in range(len(player)):
                if playersuit[0] == "Spades":
                    if player[0] != 10:
                        pCards += "♠️" + "♠️".join(str(player[0])) + "  "
                    else:
                        pCards += "♠️10  "
                elif playersuit[0] == "Hearts":
                    if player[0] != 10:
                        pCards += "♥️" + "♥️".join(str(player[0])) + "  "
                    else:
                        pCards += "♥️10  "
                elif playersuit[0] == "Diamonds":
                    if player[0] != 10:
                        pCards += "♦️" + "♦️".join(str(player[0])) + "  "
                    else:
                        pCards += "♦️10  "
                elif playersuit[0] == "Clubs":
                    if player[0] != 10:
                        pCards += "♣️" + "♣️".join(str(player[0])) + "  "
                    else:
                        pCards += "♣️10  "
                else:
                    pass
                if playersuit[1] == "Spades":
                    if player[1] != 10:
                        pCards += "♠️" + "♠️".join(str(player[1]))
                    else:
                        pCards += "♠️10  "
                elif playersuit[1] == "Hearts":
                    if player[1] != 10:
                        pCards += "♥️" + "♥️".join(str(player[1]))
                    else:
                        pCards += "♥️10  "
                elif playersuit[1] == "Diamonds":
                    if player[1] != 10:
                        pCards += "♦️" + "♦️".join(str(player[1]))
                    else:
                        pCards += "♦️10  "
                elif playersuit[1] == "Clubs":
                    if player[1] != 10:
                        pCards += "♣️" + "♣️".join(str(player[1]))
                    else:
                        pCards += "♣️10  "
                else:
                    pass

                if playersuit[0] == "Spades":
                    if dealer[0] != 10:
                        dCards += "♠️" + "♠️".join(str(dealer[0])) + "  " + "❔"
                    else:
                        dCards += "♠️10  ❔"
                elif playersuit[0] == "Hearts":
                    if dealer[0] != 10:
                        dCards += "♥️" + "♥️".join(str(dealer[0])) + "  " + "❔"
                    else:
                        dCards += "♥️10  ❔"
                elif playersuit[0] == "Diamonds":
                    if dealer[0] != 10:
                        dCards += "♦️" + "♦️".join(str(dealer[0])) + "  " + "❔"
                    else:
                        dCards += "♦️10  ❔"
                elif playersuit[0] == "Clubs":
                    if dealer[0] != 10:
                        dCards += "♣️" + "♣️".join(str(dealer[0])) + "  " + "❔"
                    else:
                        dCards += "♣️10  ❔"
                else:
                    pass

                tot = "Total = " + str(total)
                main = discord.Embed(title="Blackjack", color=0xDFFF00)
                main.set_thumbnail(url=hostAvatar)
                main.add_field(name=pCards, value=tot, inline=True)
                main.add_field(name=dCards, value="Total = ❔", inline=True)
                main.timestamp = datetime.datetime.now()
                hit = Button(style=ButtonStyle.green, label="Hit")
                stand = Button(style=ButtonStyle.green, label="Stand")
                await blackjack.edit(embed=main, components=[[hit, stand]])

                fail = False
                res = await bot.wait_for("button_click", check=check)
                user = res.component.label
                if res.user.id == userid:
                    if user == "Hit":
                        await res.respond(type=6)
                        suit = random.randint(0, 3)
                        num = random.randint(1, len(cards[suit]) - 1)
                        chosen = cards[suit][num]
                        del (cards[suit][num])
                        player.append(chosen)
                        playersuit.append(cards[suit][0])
                        num = cardValue(pVal, player[2])
                        total += num
                        total = checkCount(pVal, total)

                        if total <= 21:
                            safe = True
                            x = 2
                        else:
                            safe = False
                            fail = "You Lost " + str(bet) + " emblems"
                            main = discord.Embed(title="Blackjack", color=0xDFFF00)
                            main.set_thumbnail(url=hostAvatar)
                            main.add_field(name="Bust", value=fail, inline=True)
                            main.timestamp = datetime.datetime.now()
                            # again = Button(style=ButtonStyle.green, label="Play Again")
                            await blackjack.edit(embed=main, components=[])

                            # res = await bot.wait_for("button_click", check=check)
                            # user = res.component.label
                            # if res.user.id == userid:
                            # if user == "Play Again":
                            # blackjack()
                        while safe is True:
                            if res.user.id == userid:
                                if playersuit[x] == "Spades":
                                    if player[x] != 10:
                                        pCards += "♠️" + "♠️".join(str(player[x])) + "  "
                                    else:
                                        pCards += "♠️10  "
                                elif playersuit[x] == "Hearts":
                                    if player[x] != 10:
                                        pCards += "♥️" + "♥️".join(str(player[x])) + "  "
                                    else:
                                        pCards += "♥️10  "
                                elif playersuit[x] == "Diamonds":
                                    if player[x] != 10:
                                        pCards += "♦️" + "♦️".join(str(player[x])) + "  "
                                    else:
                                        pCards += "♦️10  "
                                elif playersuit[x] == "Clubs":
                                    if player[x] != 10:
                                        pCards += "♣️" + "♣️".join(str(player[x])) + "  "
                                    else:
                                        pCards += "♣️10  "
                                else:
                                    pass
                            tot = "Total = " + str(total)
                            main = discord.Embed(title="Blackjack", color=0xDFFF00)
                            main.set_thumbnail(url=hostAvatar)
                            main.add_field(name=pCards, value=tot, inline=True)
                            main.add_field(name=dCards, value="Total = ❔", inline=True)
                            main.timestamp = datetime.datetime.now()
                            hit = Button(style=ButtonStyle.green, label="Hit")
                            stand = Button(style=ButtonStyle.green, label="Stand")
                            await blackjack.edit(embed=main, components=[[hit, stand]])
                            res = await bot.wait_for("button_click", check=check)
                            user = res.component.label
                            if res.user.id == userid:
                                if user == "Hit":
                                    suit = random.randint(0, 3)
                                    num = random.randint(1, len(cards[suit]) - 1)
                                    chosen = cards[suit][num]
                                    del (cards[suit][num])
                                    player.append(chosen)
                                    playersuit.append(cards[suit][0])
                                    num = cardValue(pVal, player[x + 1])
                                    total += num
                                    total = checkCount(pVal, total)
                                    if total <= 21:
                                        safe = True
                                        x += 1
                                    else:
                                        safe = False
                                        fail = "You Lost " + str(bet) + " emblems"
                                        main = discord.Embed(title="Blackjack", color=0xDFFF00)
                                        main.set_thumbnail(url=hostAvatar)
                                        main.add_field(name="Bust", value=fail, inline=True)
                                        main.timestamp = datetime.datetime.now()
                                        # again = Button(style=ButtonStyle.green, label="Play Again")
                                        await blackjack.edit(embed=main, components=[])

                                        # res = await bot.wait_for("button_click", check=check)
                                        # user = res.component.label
                                        # if res.user.id == userid:
                                        # if user == "Play Again":
                                        # blackjack()
                                elif user == "Stand":
                                    safe = False
                                    try:
                                        banker = int(dealer[0] + dealer[1])
                                    except:
                                        try:
                                            banker = int(dealer[0])
                                        except:
                                            try:
                                                banker = int(dealer[0])
                                            except:
                                                banker = 10

                                    b1 = cardValue(dVal, dealer[0])
                                    banker = b1
                                    b2 = cardValue(dVal, dealer[1])
                                    banker += b2
                                    y = 2
                                    while banker < 17:
                                        suit = random.randint(0, 3)
                                        num = random.randint(1, len(cards[suit]) - 1)
                                        chosen = cards[suit][num]
                                        del (cards[suit][num])
                                        dealer.append(chosen)
                                        dealersuit.append(cards[suit][0])
                                        b = cardValue(dVal, dealer[y])
                                        banker += b
                                        banker = checkCount(dVal, banker)
                                    if banker >= total and banker <= 21:
                                        fail = "You Lost " + str(bet) + " emblems"
                                        main = discord.Embed(title="Blackjack", color=0xDFFF00)
                                        main.set_thumbnail(url=hostAvatar)
                                        main.add_field(name="Dealer beat you", value=fail, inline=True)
                                        main.timestamp = datetime.datetime.now()
                                        await blackjack.edit(embed=main, components=[])

                                    elif banker > 21:
                                        winning = "You won " + str(bet) + " emblems"
                                        main = discord.Embed(title="Blackjack", color=0xDFFF00)
                                        main.set_thumbnail(url=hostAvatar)
                                        main.add_field(name="Dealer Bust", value=winning, inline=True)
                                        main.timestamp = datetime.datetime.now()
                                        # again = Button(style=ButtonStyle.green, label="Play Again")
                                        await blackjack.edit(embed=main, components=[])
                                        ticketChange(userid, 2 * bet)
                                    else:
                                        winning = "You won " + str(bet) + " emblems"
                                        main = discord.Embed(title="Blackjack", color=0xDFFF00)
                                        main.set_thumbnail(url=hostAvatar)
                                        main.add_field(name="You beat the banker", value=winning, inline=True)
                                        main.timestamp = datetime.datetime.now()
                                        # again = Button(style=ButtonStyle.green, label="Play Again")
                                        await blackjack.edit(embed=main, components=[])
                                        ticketChange(userid, 2 * bet)
                                await res.respond(type=6)
                    elif user == "Stand":
                        try:
                            banker = int(dealer[0] + dealer[1])
                        except:
                            try:
                                banker = int(dealer[0])
                            except:
                                try:
                                    banker = int(dealer[0])
                                except:
                                    banker = 10

                        b1 = cardValue(dVal, dealer[0])
                        banker = b1
                        b2 = cardValue(dVal, dealer[1])
                        banker += b2
                        y = 2
                        while banker < 17:
                            suit = random.randint(0, 3)
                            num = random.randint(1, len(cards[suit]) - 1)
                            chosen = cards[suit][num]
                            del (cards[suit][num])
                            dealer.append(chosen)
                            dealersuit.append(cards[suit][0])
                            b = cardValue(dVal, dealer[y])
                            banker += b
                        if banker > total and banker <= 21:
                            fail = "You Lost " + str(bet) + " emblems"
                            main = discord.Embed(title="Blackjack", color=0xDFFF00)
                            main.set_thumbnail(url=hostAvatar)
                            main.add_field(name="Dealer beat you", value=fail, inline=True)
                            main.timestamp = datetime.datetime.now()
                            await blackjack.edit(embed=main, components=[])
                        elif banker > 21:
                            winning = "You won " + str(bet) + " emblems"
                            main = discord.Embed(title="Blackjack", color=0xDFFF00)
                            main.set_thumbnail(url=hostAvatar)
                            main.add_field(name="Dealer Bust", value=winning, inline=True)
                            main.timestamp = datetime.datetime.now()
                            # again = Button(style=ButtonStyle.green, label="Play Again")
                            await blackjack.edit(embed=main, components=[])
                            ticketChange(userid, 2 * bet)
                        else:
                            winning = "You won " + str(bet) + " emblems"
                            main = discord.Embed(title="Blackjack", color=0xDFFF00)
                            main.set_thumbnail(url=hostAvatar)
                            main.add_field(name="You beat the banker", value=winning, inline=True)
                            main.timestamp = datetime.datetime.now()
                            # again = Button(style=ButtonStyle.green, label="Play Again")
                            await blackjack.edit(embed=main, components=[])
                            ticketChange(userid, 2 * bet)
                    await res.respond(type=6)


                else:
                    await res.respond(content="This is not your game! Play your own by typing /blackjack")
            else:
                winning = "You won " + str(1.5 * bet) + " emblems"
                main = discord.Embed(title="Blackjack", color=0xDFFF00)
                main.set_thumbnail(url=hostAvatar)
                main.add_field(name="Blackjack", value=winning, inline=True)
                main.timestamp = datetime.datetime.now()
                # again = Button(style=ButtonStyle.green, label="Play Again")
                await blackjack.edit(embed=main, components=[])
                ticketChange(userid, int(2.5 * bet))

                # res = await bot.wait_for("button_click", check=check)
                # user = res.component.label
                # if res.user.id == userid:
                # if user == "Play Again":
                # blackjack()
        else:
            await res.respond(content="This is not your game! Play your own by typing /blackjack")

    else:
        await res.respond(content="This is not your game! Play your own by typing /blackjack")
    await res.respond(type=6)


@slash.slash(name="ldb", description="View emblems leaderboard")
async def ldb(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][1])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='EMBLEMS LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="carryldb", description="View top msk carriers")
async def carryldb(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][2])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='MSK CARRY LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="helpedldb", description="View biggest msk nubs")
async def helpedldb(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][3])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='MSK NUB LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="hostldb", description="View biggest endurance hosters")
async def hostldb(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][4])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='ENDURANCE RUNS LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="leeches", description="View biggest endurance leechers")
async def leeches(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][5])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='LEECH LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="host", description="Host an endurance")
async def host(ctx):
    name = ctx.author
    userid = ctx.author.id
    hostName = ctx.author.name
    host_name = ctx.author.name
    host_avatar = ctx.author.avatar_url
    hostAvatar = ctx.author.avatar_url
    botChannel = 976418819532808192

    def checkUser(author, userid):
        ids = []
        for key in db.keys():
            ids.append(db[key][0])
        if userid in ids:
            pass
        else:
            db[userid] = [userid, 20, 0, 0, 0, 0, 0]

    checkUser(name, userid)

    def ticketUpdate(userid, tickets):
        ids = []
        emblems = []
        for key in db.keys():
            ids.append(db[key][0])
            emblems.append(db[key][1])
        num = emblems[ids.index(userid)]
        if num + tickets >= 0:
            return True
        else:
            return False

    if ctx.channel.id == botChannel:
        if True:
            def check(author, channel):
                def inner_check(message):
                    return message.author == author and channel == botChannel

                return inner_check

            await ctx.send('Epic? or type /cancel to cancel')
            epicName = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
            if epicName.content in illegal:
                epicName = int(epicName.content)

            area = -1
            while area == -1:
                await ctx.send(
                    'Please enter the zone, follow the pattern below or type /cancel to cancel: \nTwine Peaks - 4 \nCanny Valley - 3 \nPlankerton - 2 \nStonewood - 1 \n')
                zone = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
                try:
                    area = int(zone.content)
                    if area == 1:
                        zone = "Stonewood"
                        cost = stone
                    elif area == 2:
                        zone = "Plankerton"
                        cost = plank
                    elif area == 3:
                        zone = "Canny Valley"
                        cost = canny
                    elif area == 4:
                        zone = "Twine Peaks"
                        cost = twine
                    else:
                        area = -1
                        await ctx.send("Enter 1,2,3 or 4 only")
                except ValueError:
                    if zone.content in illegal:
                        area = int(zone.content)
                    else:
                        zone = -1
                        await ctx.send("Enter 1,2,3 or 4 only")

            spots = -1
            while spots == -1:
                await ctx.send('Number of seats? or type /cancel to cancel?')
                seats = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
                try:
                    spots = int(seats.content)
                    if spots == 1 or spots == 2 or spots == 3:
                        spots = spots
                    else:
                        spots = -1
                        await ctx.send("Enter 1,2 or 3 only")
                except:
                    if seats.content in illegal:
                        spots = int(seats.content)
                    else:
                        spots = -1
                        await ctx.send("Enter 1,2 or 3 only")

            sea = -1
            while sea == -1:
                await ctx.send('Wave? or type /cancel to cancel')
                wave = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
                try:
                    sea = int(wave.content)
                    if 25 <= sea <= 30:
                        sea = sea
                    else:
                        sea = -1
                        await ctx.send("Only waves 25-30 acceptable")
                except:
                    if wave.content in illegal:
                        sea = int(wave.content)
                    else:
                        sea = -1
                        await ctx.send("Only waves 25-30 acceptable")

            Endurance = get(ctx.guild.roles, name='Endurance')
            location = bot.get_channel(925926796531236864)
            await location.send(f"{Endurance.mention}")
            enduranceHost = discord.Embed(title=f"{host_name}\'s Endurance", color=0xDFFF00)
            # enduranceHost.set_image(url=f"{host_avatar}")
            enduranceHost.set_thumbnail(url=host_avatar)
            enduranceHost.add_field(name="Epic Username", value=epicName.content, inline=False)
            enduranceHost.add_field(name="Zone", value=zone, inline=True)
            enduranceHost.add_field(name="Wave", value=wave.content, inline=True)
            enduranceHost.add_field(name="Seats", value=seats.content, inline=True)
            enduranceHost.add_field(name="Seat 1", value="Available", inline=False)
            if spots > 1:
                enduranceHost.add_field(name="Seat 2", value="Available", inline=False)
                if spots > 2:
                    enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

            enduranceHost.timestamp = datetime.datetime.now()
            one = Button(style=ButtonStyle.green, label="Claim", id="embed1")
            two = Button(style=ButtonStyle.red, label="Unclaim", id="embed2")
            three = Button(style=ButtonStyle.grey, label="End", id="embed3")
            four = Button(style=ButtonStyle.grey, label="Cancel", id="embed4")

            embed1 = discord.Embed(title="Claim", description="You have claimed a spot", color=discord.Colour.blue())
            embed2 = discord.Embed(title="Unclaim", description="You have unclaimed a spot", color=discord.Colour.red())
            embed3 = discord.Embed(title="End", description="You have ended the run", color=discord.Colour.greyple())
            embed4 = discord.Embed(title="Cancel", description="You have cancelled the run",
                                   color=discord.Colour.greyple())

            msg = await location.send(embed=enduranceHost, components=[[one, two, three, four]])
            t1 = datetime.datetime.now()
            embedid = msg.id
            buttons = {"embed1": embed1, "embed2": embed2, "embed3": embed3, "embed4": embed4}
            leechers = []

            stripes = spots
            buttonid = msg.id

            def check(res):
                return res.channel == location and msg == res.message

            def ticketChange(userid, tickets):
                for key in db.keys():
                    if db[key][0] == userid:
                        db[key][1] += tickets

            checkUser(name, userid)

            while True:
                res = await bot.wait_for("button_click", check=check)
                user = res.component.label
                if user == "Claim":
                    checkUser(res.user, res.user.id)
                    if ticketUpdate(res.user.id, -cost) is True:
                        if stripes > 0:
                            claimerid = res.user.id
                            if claimerid not in leechers:
                                if claimerid != userid:
                                    stripes -= 1
                                    leechers.append(claimerid)
                                    # update embed seats
                                    enduranceHost = discord.Embed(title=f"{host_name}\'s Endurance", color=0xDFFF00)
                                    enduranceHost.set_thumbnail(url=host_avatar)
                                    enduranceHost.add_field(name="Epic Username", value=epicName.content, inline=False)
                                    enduranceHost.add_field(name="Zone", value=zone, inline=True)
                                    enduranceHost.add_field(name="Wave", value=wave.content, inline=True)
                                    enduranceHost.add_field(name="Seats", value=stripes, inline=True)
                                    if len(leechers) == 1:
                                        enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                        if spots > 1:
                                            enduranceHost.add_field(name="Seat 2", value="Available", inline=False)
                                            if spots > 2:
                                                enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

                                    if len(leechers) == 2:
                                        enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                        enduranceHost.add_field(name="Seat 2", value=f"<@{leechers[1]}>", inline=False)
                                        if spots > 2:
                                            enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

                                    if len(leechers) == 3:
                                        enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                        enduranceHost.add_field(name="Seat 2", value=f"<@{leechers[1]}>", inline=False)
                                        enduranceHost.add_field(name="Seat 3", value=f"<@{leechers[2]}>", inline=False)

                                    enduranceHost.timestamp = datetime.datetime.now()
                                    await msg.edit(embed=enduranceHost, components=[[one, two, three, four]])
                                    sad = await ctx.author.guild.fetch_member(userid)
                                    await sad.send(f"{res.user.name} claimed your endurance")
                                    correct = ticketChange(claimerid, -1 * cost)
                                    correct = ticketChange(userid, cost)
                                else:
                                    await res.respond(content="You cannot claim your own endurance!")
                            else:
                                await res.respond(content="You have already claimed!")
                        else:
                            await res.respond(content="There are no more spots!")

                elif user == "Unclaim":
                    checkUser(res.user, res.user.id)
                    claims = 0
                    unclaimerid = res.user.id
                    try:
                        for i in range(0, 2):
                            if leechers[i] == unclaimerid:
                                leechers.remove(unclaimerid)
                                claims += 1
                        if claims == 0:
                            await res.respond(content="You have not claimed!")
                    except:
                        if claims == 0:
                            await res.respond(content="You have not claimed!")
                        else:
                            stripes += 1
                            enduranceHost = discord.Embed(title=f"{host_name}\'s Endurance", color=0xDFFF00)
                            enduranceHost.set_thumbnail(url=host_avatar)
                            enduranceHost.add_field(name="Epic Username", value=epicName.content, inline=False)
                            enduranceHost.add_field(name="Zone", value=zone, inline=True)
                            enduranceHost.add_field(name="Wave", value=wave.content, inline=True)
                            enduranceHost.add_field(name="Seats", value=spots - len(leechers), inline=True)
                            if len(leechers) == 0:
                                enduranceHost.add_field(name="Seat 1", value="Available", inline=False)
                                if spots > 1:
                                    enduranceHost.add_field(name="Seat 2", value="Available", inline=False)
                                    if spots > 2:
                                        enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

                            if len(leechers) == 1:
                                enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                if spots > 1:
                                    enduranceHost.add_field(name="Seat 2", value="Available", inline=False)
                                    if spots > 2:
                                        enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

                            if len(leechers) == 2:
                                enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                enduranceHost.add_field(name="Seat 2", value=f"<@{leechers[1]}>", inline=False)
                                if spots > 2:
                                    enduranceHost.add_field(name="Seat 3", value="Available", inline=False)

                            if len(leechers) == 3:
                                enduranceHost.add_field(name="Seat 1", value=f"<@{leechers[0]}>", inline=False)
                                enduranceHost.add_field(name="Seat 2", value=f"<@{leechers[1]}>", inline=False)
                                enduranceHost.add_field(name="Seat 3", value=f"<@{leechers[2]}>", inline=False)

                            enduranceHost.timestamp = datetime.datetime.now()
                            await msg.edit(embed=enduranceHost, components=[[one, two, three, four]])
                            happy = await ctx.author.guild.fetch_member(userid)
                            await happy.send(f"{res.user.name} unclaimed your endurance")
                            correct = ticketChange(unclaimerid, cost)
                            correct = ticketChange(userid, -cost)

                elif user == "End":
                    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
                    endid = res.user.id
                    if endid == userid or role in res.user.roles:
                        a = datetime.timedelta(minutes=5, seconds=0)
                        t2 = datetime.datetime.now()
                        time = t2 - t1
                        people = ''
                        if len(leechers) == 0:
                            claimers = 'No Claims'
                            if time <= a:
                                people = 'Not enough time, no emblems awarded'
                            else:
                                people = 'Emblems awarded'
                        else:
                            claimers = 'Claimers:'
                            for leech in leechers:
                                boo = await ctx.author.guild.fetch_member(leech)
                                people += str(boo.name) + ' '
                        enduranceHost = discord.Embed(title="Endurance Completed", color=0xDFFF00)
                        enduranceHost.set_author(name=host_name, icon_url=host_avatar)
                        enduranceHost.add_field(name=claimers, value=people, inline=False)
                        enduranceHost.timestamp = datetime.datetime.now()
                        await msg.edit(embed=enduranceHost, components=[])
                        for key in db.keys():
                            if db[key][0] in leechers:
                                db[key][5] += 1
                            elif db[key][0] == endid:
                                db[key][4] += 1
                            else:
                                pass
                        a = datetime.timedelta(minutes=5, seconds=0)
                        t2 = datetime.datetime.now()
                        time = t2 - t1
                        if time >= a:
                            spare = spots - len(leechers)
                            correct = ticketChange(userid, spare * cost)
                        else:
                            pass
                    else:
                        await res.respond(content="You can not end somebody else's endurance!")

                elif user == "Cancel":
                    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
                    cancelid = res.user.id
                    if cancelid == userid or role in res.user.roles:
                        enduranceHost = discord.Embed(title="Endurance Cancelled", color=0xDFFF00)
                        enduranceHost.set_author(name=host_name, icon_url=host_avatar)
                        enduranceHost.timestamp = datetime.datetime.now()
                        await msg.edit(embed=enduranceHost, components=[])
                        for leech in leechers:
                            correct = ticketChange(leech, cost)
                            correct = ticketChange(userid, -cost)
                    else:
                        await res.respond(content="You can not cancel somebody else's endurance!")
                await res.respond(type=6)
    else:
        botChannelName = bot.get_channel("botChannel")
        await ctx.send(content=f"<@{userid}> please use "f"<#{botChannel}>")


@slash.slash(name="highorlow", description="Play a game of higher or lower fro emblems leaderboard")
async def highorlow(ctx):
    end = False
    streak = 0
    name = ctx.author
    userid = ctx.author.id
    hostName = ctx.author.name
    hostAvatar = ctx.author.avatar_url
    botChannel = 976418819532808192

    def check(author, channel):
        def inner_check(message):
            return message.author == author and channel == botChannel

        return inner_check

    def check(res):
        return res.channel.id == botChannel and embed == res.message

    def getEmb(id):
        for key in db.keys():
            if db[key][0] == id:
                return db[key][1]

    def getNames(first):
        x = False
        emblems = getEmb(first)
        people = []
        for key in db.keys():
            people.append(key)
        while x == False:
            player = people[random.randint(0, len(db.keys()) - 1)]
            playerid = db[player][0]
            playeremb = db[player][1]
            if playeremb != emblems:
                x = True
            else:
                pass
        return playerid, playeremb

    if ctx.channel.id == botChannel:
        main = discord.Embed(title="Welcome to Higher or Lower", color=0xDFFF00)
        main.set_thumbnail(url=hostAvatar)
        main.add_field(name="Rules",
                       value="Click the button Higher or Lower depending on your answer\nYou have a time limit of 10 seconds per round\nThe next round will be started automatically after you guess correct\nHow long can you keep your streak?",
                       inline=True)
        main.timestamp = datetime.datetime.now()
        play = Button(style=ButtonStyle.green, label="Play")
        embed = await ctx.send(embed=main, components=[[play]])
        while True:
            res = await bot.wait_for("button_click", check=check)
            user = res.component.label
            if res.user.id == userid:
                await res.respond(type=6)
                end = False
                timeFail = False
                wrong = False
                newplayer, newemb = getNames(userid)
                playeremb = getEmb(userid)
                player = userid
                playerName = await ctx.author.guild.fetch_member(player)
                newName = await ctx.author.guild.fetch_member(newplayer)
                main = discord.Embed(title="Welcome to Higher or Lower", color=0xDFFF00)
                main.set_thumbnail(url=hostAvatar)
                main.add_field(name=playerName.name, value=playeremb, inline=True)
                main.add_field(name=newName.name, value="?", inline=True)
                main.timestamp = datetime.datetime.now()
                higher = Button(style=ButtonStyle.green, label="Higher")
                lower = Button(style=ButtonStyle.red, label="Lower")
                await embed.edit(embed=main, components=[[higher, lower]])
                if "yes" == "yes":
                    end = False
                    while end == False:
                        try:
                            res = await bot.wait_for("button_click", check=check, timeout=10)
                            user = res.component.label
                            claimerID = res.user.id
                            if claimerID == userid:
                                if user == "Higher":
                                    await res.respond(type=6)
                                    if newemb > playeremb:
                                        wrong = False
                                        streak += 1
                                        player = newplayer
                                        playeremb = newemb
                                        newplayer, newemb = getNames(player)

                                    else:
                                        wrong = True
                                elif user == "Lower":
                                    await res.respond(type=6)
                                    if newemb < playeremb:
                                        wrong = False
                                        streak += 1
                                        player = newplayer
                                        playeremb = newemb
                                        newplayer, newemb = getNames(player)

                                    else:
                                        wrong = True
                                if wrong == True:
                                    end = True
                                else:
                                    playerName = await ctx.author.guild.fetch_member(player)
                                    newName = await ctx.author.guild.fetch_member(newplayer)
                                    main = discord.Embed(title="Welcome to Higher or Lower", color=0xDFFF00)
                                    main.set_thumbnail(url=hostAvatar)
                                    main.add_field(name=playerName.name, value=playeremb, inline=True)
                                    main.add_field(name=newName.name, value="?", inline=True)
                                    main.timestamp = datetime.datetime.now()
                                    higher = Button(style=ButtonStyle.green, label="Higher")
                                    lower = Button(style=ButtonStyle.red, label="Lower")
                                    await embed.edit(embed=main, components=[[higher, lower]])
                            else:
                                await res.respond(content="This is not your game!")
                        except asyncio.TimeoutError:
                            end = True
                            timeFail = True
                    for key in db.keys():
                        if db[key][0] == userid:
                            highScore = db[key][6]
                            if streak > highScore:
                                highScore = streak
                                db[key][6] = highScore
                    main = discord.Embed(color=0xDFFF00)
                    main.set_thumbnail(url=hostAvatar)
                    if timeFail == True:
                        main.add_field(name="GAMEOVER", value="You ran out of time", inline=False)
                    else:
                        main.add_field(name="GAMEOVER", value="Wrong choice", inline=False)
                    main.add_field(name="Your score:", value=streak, inline=True)
                    main.add_field(name="Your high score: ", value=highScore, inline=True)
                    main.timestamp = datetime.datetime.now()
                    embed = await embed.edit(embed=main, components=[])
            else:
                await res.respond(content="This is not your game!")
    else:
        await ctx.send(content=f"<@{userid}> please use "f"<#{botChannel}>")


@slash.slash(name="topmali", description="Biggest Malivore fans")
async def topmali(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][7])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='MOST PET MALIVORES', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="potofluck", description="Start a prize pool for emblems")
async def potofluck(ctx):
    players = []
    prize = 0
    botChannel = 976418819532808192
    locationID = 976779874532478986
    location = bot.get_channel(locationID)

    # Get input for time and cost to enter

    def check(author, channel):
        def inner_check(message):
            return message.author == author and channel == botChannel

        return inner_check

    def ticketUpdate(userid, tickets):
        ids = []
        emblems = []
        for key in db.keys():
            ids.append(db[key][0])
            emblems.append(db[key][1])
        num = emblems[ids.index(userid)]
        if num + tickets >= 0:
            return True
        else:
            return False

    def ticketChange(userid, tickets):
        for key in db.keys():
            if db[key][0] == userid:
                db[key][1] += tickets

    def checkUser(author, userid):
        ids = []
        for key in db.keys():
            ids.append(db[key][0])
        if userid in ids:
            pass
        else:
            db[userid] = [userid, 20, 0, 0, 0, 0, 0]

    await ctx.send("Enter the join cost")
    cost = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
    money = False
    while not money:
        try:
            cost = int(cost.content)
            money = True
        except ValueError:
            if cost.content in illegal:
                cost = int(cost.content)
            else:
                await ctx.channel.send("Enter an integer only")
                cost = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)

    await ctx.send("Enter the time e.g. 1h 34m 18s")
    times = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)
    clock = False
    while not clock:
        try:
            timers = (times.content).split(" ")
            try:
                if len(timers[0].split("h")) > 1:
                    h = timers[0].split("h")[0]
                    timers.remove(h + "h")
                else:
                    h = 0
            except:
                h = 0
            try:
                if len(timers[0].split("m")) > 1:
                    m = timers[0].split("m")[0]
                    timers.remove(m + "m")
                else:
                    m = 0
            except:
                m = 0

            try:
                if len(timers[0].split("s")) > 1:
                    s = timers[0].split("s")[0]
                    timers.remove(s + "s")
                else:
                    s = 0
            except:
                s = 0
            if h == 0 and m == 0 and s == 0:
                h = "m"
            time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            clock = True
        except:
            if times.content in illegal:
                cost = int(cost.content)
            else:
                await ctx.channel.send("Enter the time e.g. 1h 34m 18s")
                times = await bot.wait_for("message", check=check(ctx.author, ctx.channel.id), timeout=30)

    # msk = get(ctx.channel.guild.roles, name='msk_pings')
    # await location.send(f"{msk.mention}")
    emby = str(cost) + " emblems"
    endTime = datetime.datetime.now() + time
    potEmbed = discord.Embed(title="Pot of Luck", color=0xDFFF00)
    potEmbed.add_field(name="Join the pot of luck for:", value=emby, inline=False)
    potEmbed.add_field(name="Total Prize:", value="0", inline=True)
    potEmbed.add_field(name="Number of people:", value="0", inline=True)
    potEmbed.add_field(name="\u200b", value="Ends:", inline=False)
    potEmbed.timestamp = endTime
    join = Button(style=ButtonStyle.green, label="Join")
    leave = Button(style=ButtonStyle.red, label="Leave")
    msg = await location.send(embed=potEmbed, components=[[join, leave]])

    def check(res):
        return res.channel.id == locationID and msg == res.message

    end = False
    t1 = datetime.datetime.now()
    while not end:
        try:
            res = await bot.wait_for("button_click", check=check, timeout=1)
            user = res.component.label
            if user == "Join":
                checkUser(res.user, res.user.id)
                joined = ticketUpdate(res.user.id, -int(cost))
                if res.user.id not in players:
                    if joined is True:
                        players.append(res.user.id)
                        prize += int(cost)
                        ticketChange(res.user.id, -int(cost))
                        potEmbed = discord.Embed(title="Pot of Luck", color=0xDFFF00)
                        potEmbed.add_field(name="Join the pot of luck for:", value=emby, inline=False)
                        potEmbed.add_field(name="Total Prize:", value=str(prize), inline=True)
                        potEmbed.add_field(name="Number of people:", value=str(len(players)), inline=True)
                        potEmbed.add_field(name="\u200b", value="Ends:", inline=False)
                        potEmbed.timestamp = endTime
                        await msg.edit(embed=potEmbed)
                    else:
                        await res.respond(content="You do not have enough emblems to join!")
                else:
                    await res.respond(content="You have already joined!")
            elif user == "Leave":
                checkUser(res.user, res.user.id)
                if res.user.id in players:
                    players.remove(res.user.id)
                    prize -= int(cost)
                    ticketChange(res.user.id, int(cost))
                    potEmbed = discord.Embed(title="Pot of Luck", color=0xDFFF00)
                    potEmbed.add_field(name="Join the pot of luck for:", value=emby, inline=False)
                    potEmbed.add_field(name="Total Prize:", value=str(prize), inline=True)
                    potEmbed.add_field(name="Number of people:", value=str(len(players)), inline=True)
                    potEmbed.add_field(name="\u200b", value="Ends:", inline=False)
                    potEmbed.timestamp = endTime
                    await msg.edit(embed=potEmbed)
                else:
                    await res.respond(content="You have not joined")
            else:
                pass
            await res.respond(type=6)
        except asyncio.TimeoutError:
            t2 = datetime.datetime.now()
            if t2 - t1 >= time:
                end = True
            else:
                pass
    if len(players) > 0:
        winnerPlace = random.randint(0, len(players) - 1)
        winnerID = players[winnerPlace]
        winner = await ctx.author.guild.fetch_member(winnerID)
        ticketChange(winnerID, int(prize))
        potEmbed = discord.Embed(color=0xDFFF00)
        # potEmbed.set_thumbnail(url=winner.avatar)
        potEmbed.add_field(name="WINNER", value=f"<@{winnerID}>")
        potEmbed.add_field(name="Total Prize:", value=str(prize), inline=True)
        potEmbed.add_field(name="Total people:", value=str(len(players)), inline=True)
        potEmbed.timestamp = datetime.datetime.now()
        await msg.edit(embed=potEmbed, components=[])
    else:
        potEmbed = discord.Embed(title="Nobody Joined", color=0xDFFF00)
        potEmbed.add_field(name="Time ran out", value="\u200b", inline=True)
        potEmbed.timestamp = datetime.datetime.now()
        await msg.edit(embed=potEmbed, components=[])


@slash.slash(name="mali", description="Pet Malivore")
async def mali(ctx):
    mali = discord.Embed(title="Queen Malivore", color=0xDFFF00)
    mali.set_image(
        url="https://cdn.discordapp.com/avatars/538394329333497865/c55e041740426ec104c49f7d5c5b2081.png?size=1024")
    mali.add_field(name="Hey You! Make sure to pet your Queen", value="Pets = 0", inline=False)
    mali.timestamp = datetime.datetime.now()
    pet = Button(style=ButtonStyle.green, label="Pet")
    msg = await ctx.send(embed=mali, components=[[pet]])
    pot = 0

    def check(res):
        return msg == res.message

    while True:
        res = await bot.wait_for("button_click", check=check)
        user = res.component.label
        if user == "Pet":
            for key in db.keys():
                if db[key][0] == res.user.id:
                    db[key][7] += 1
            await res.respond(type=6)
            pot += 1
            petty = str("Pets: " + str(pot))
            mali = discord.Embed(title="Queen Malivore", color=0xDFFF00)
            mali.set_image(url="https://cdn.discordapp.com/emojis/965249410986565682.gif")
            mali.add_field(name="Good Pet, Malivore is now a happy bunny", value=petty, inline=True)
            mali.timestamp = datetime.datetime.now()
            await msg.edit(embed=mali, components=[])

            await asyncio.sleep(5)
            mali = discord.Embed(title="Queen Malivore", color=0xDFFF00)
            mali.set_image(
                url="https://cdn.discordapp.com/avatars/538394329333497865/c55e041740426ec104c49f7d5c5b2081.png?size=1024")
            mali.add_field(name="Hey You! Make sure to pet your Queen", value=petty, inline=False)
            mali.timestamp = datetime.datetime.now()
            pet = Button(style=ButtonStyle.green, label="Pet")
            await msg.edit(embed=mali, components=[[pet]])


@slash.slash(name="highscore", description="Highest scores on higher or lower")
async def highscore(ctx):
    arr = []
    users = []

    def bubbleSort(arr, users):
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    users[j], users[j + 1] = users[j + 1], users[j]

    for key in db.keys():
        arr.append(db[key][6])
        users.append(db[key][0])
    bubbleSort(arr, users)
    leaderboard = discord.Embed(color=0xDFFF00)
    names = ''
    value = ''
    for i in range(0, 19):
        try:
            new = await ctx.author.guild.fetch_member(users[i])
            new = new.name
            a = (':  ' + ((20 - (len(new))) * '  '))
            newbie = (str(i + 1) + '. ' + str(new) + a + str(arr[i]) + '\n')
            names += newbie
        except:
            pass
    leaderboard.add_field(name='HIGH SCORE LEADERBOARD', value=f'{names}', inline=True)
    await ctx.send(embed=leaderboard)


@slash.slash(name="roulette", description="Pay to join, could win all or be temp banned")
async def roulette(ctx):
    players = []
    maxPlayers = 2
    joinCost = 20
    prize = 0
    name = ctx.author
    userid = ctx.author.id
    hostName = ctx.author.name
    hostAvatar = ctx.author.avatar_url
    botChannel = 976418819532808192
    locationID = 980184740906811404
    location = bot.get_channel(locationID)

    # Get input for time and cost to enter

    def ticketUpdate(userid, tickets):
        ids = []
        emblems = []
        for key in db.keys():
            ids.append(db[key][0])
            emblems.append(db[key][1])
        num = emblems[ids.index(userid)]
        if num + tickets >= 0:
            return True
        else:
            return False

    def ticketChange(userid, tickets):
        for key in db.keys():
            if db[key][0] == userid:
                db[key][1] += tickets

    def checkUser(author, userid):
        ids = []
        for key in db.keys():
            ids.append(db[key][0])
        if userid in ids:
            pass
        else:
            db[userid] = [userid, 20, 0, 0, 0, 0, 0]

    time = datetime.datetime.now()
    main = discord.Embed(title="Welcome to Roulette", color=0xDFFF00)
    main.set_thumbnail(url=hostAvatar)
    main.add_field(name="Number of people to join", value="\u200b", inline=True)
    main.timestamp = datetime.datetime.now()
    five = Button(style=ButtonStyle.green, label=5)
    ten = Button(style=ButtonStyle.green, label=10)
    msg = await ctx.send(embed=main, components=[[five, ten]])

    def checkPlayer(res):
        return res.user.id == userid and msg == res.message

    def check(res):
        return msg == res.message

    res = await bot.wait_for("button_click", check=checkPlayer)
    user = res.component.label
    if user == "5":
        await res.respond(type=6)
        maxPlayers = 5
    elif user == "10":
        await res.respond(type=6)
        maxPlayers = 10
    main = discord.Embed(title="All set up", color=0xDFFF00)
    main.timestamp = datetime.datetime.now()
    await msg.edit(embed=main, components=[])

    # msk = get(ctx.channel.guild.roles, name='msk_pings')
    # await location.send(f"{msk.mention}")
    emby = str(joinCost) + " emblems"
    new = str("0") + "/" + str(maxPlayers)
    potEmbed = discord.Embed(title="Roulette", color=0xDFFF00)
    potEmbed.add_field(name="Will you win 300 emblems or get 7 day ban?", value=emby, inline=False)
    potEmbed.add_field(name="Total Prize:", value=str(joinCost * maxPlayers), inline=True)
    potEmbed.add_field(name="Number of people:", value=new, inline=True)
    potEmbed.timestamp = time
    join = Button(style=ButtonStyle.green, label="Join")
    leave = Button(style=ButtonStyle.red, label="Leave")
    msg = await location.send(embed=potEmbed, components=[[join, leave]])

    end = False
    while end is False:
        res = await bot.wait_for("button_click", check=check)
        user = res.component.label
        if user == "Join":
            await res.respond(type=6)
            checkUser(res.user, res.user.id)
            joined = ticketUpdate(res.user.id, -int(joinCost))
            if res.user.id not in players:
                if joined is True:
                    players.append(res.user.id)
                    prize += int(joinCost)
                    ticketChange(res.user.id, -int(joinCost))
                    new = str(len(players)) + "/" + str(maxPlayers)
                    potEmbed = discord.Embed(title="Roulette", color=0xDFFF00)
                    potEmbed.add_field(name="Will you win 300 emblems or get 7 day ban?", value=emby, inline=False)
                    potEmbed.add_field(name="Total Prize:", value=str(joinCost * maxPlayers), inline=True)
                    potEmbed.add_field(name="Number of people:", value=new, inline=True)
                    potEmbed.timestamp = time
                    await msg.edit(embed=potEmbed)
                    if len(players) == maxPlayers:
                        end = True
                else:
                    await res.respond(content="You do not have enough emblems to join!")
            else:
                await res.respond(content="You have already joined!")
        elif user == "Leave":
            await res.respond(type=6)
            checkUser(res.user, res.user.id)
            if res.user.id in players:
                players.remove(res.user.id)
                prize -= int(joinCost)
                ticketChange(res.user.id, int(joinCost))
                new = str(len(players)) + "/" + str(maxPlayers)
                potEmbed = discord.Embed(title="Roulette", color=0xDFFF00)
                potEmbed.add_field(name="Will you win 300 emblems or get 7 day ban?", value=emby, inline=False)
                potEmbed.add_field(name="Total Prize:", value=str(joinCost * maxPlayers), inline=True)
                potEmbed.add_field(name="Number of people:", value=new, inline=True)
                potEmbed.timestamp = time
                await msg.edit(embed=potEmbed)
            else:
                await res.respond(content="You have not joined")
        else:
            pass

    winnerPlace = random.randint(0, len(players) - 1)
    winnerID = players[winnerPlace]
    winner = await ctx.author.guild.fetch_member(winnerID)
    players.remove(winnerID)
    loserPlace = random.randint(0, len(players) - 1)
    loserID = players[loserPlace]
    loser = await ctx.author.guild.fetch_member(loserID)
    ticketChange(winnerID, int(prize))
    potEmbed = discord.Embed(color=0xDFFF00)
    # potEmbed.set_thumbnail(url=winner.avatar)
    potEmbed.add_field(name="WINNER", value=f"<@{winnerID}>")
    potEmbed.add_field(name="LOSER", value=f"<@{loserID}>")
    potEmbed.timestamp = datetime.datetime.now()
    await msg.edit(embed=potEmbed, components=[])


bot.run(os.environ("TOKEN"), bot=True, reconnect=True)
