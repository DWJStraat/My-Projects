
from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
mineflayerViewer = require('prismarine-viewer').mineflayer
pvp = require('mineflayer-pvp').plugin

RANGE_GOAL = 1
BOT_USERNAME = 'MobBot'

CMDR = 'NeonMobborn'


def createbot(name):
    bot = mineflayer.createBot({
        'host': '127.0.0.1',
        'port': 25565,
        'username': name
    })
    return bot


targetlist = []
bot = createbot('MobBot0')

bot.loadPlugin(pathfinder.pathfinder)
bot.loadPlugin(pvp)
print("Started mineflayer")


@On(bot, 'spawn')
def handle(*args):
    print("I spawned 👋")
    mcData = require('minecraft-data')(bot.version)
    # mineflayerViewer(bot,
    #                  {
    #                      'port': 3007,
    #                      'firstPerson': False
    #                  })
    movements = pathfinder.Movements(bot, mcData)

    @On(bot, 'chat')
    def handleMSG(this, sender, message, *args):
        if sender and (sender == CMDR):
            if 'rally' in message:
                player = bot.players[CMDR]
                print(f'Rallying to {CMDR}')
                target = player.entity
                if not target:
                    bot.chat("Can't find a clear path!")
                    return
                pos = target.position
                bot.pathfinder.setMovements(movements)
                bot.pathfinder.setGoal(pathfinder.goals.GoalNear(
                    pos.x, pos.y, pos.z), RANGE_GOAL)
            if message.startswith('go to coordinates'):
                try:
                    x, y, z = map(lambda v: int(v), message.split(
                        "coordinates")[1].replace(",", " ").split())
                    bot.pathfinder.setMovements(movements)
                    bot.pathfinder.setGoal(
                        pathfinder.goals.GoalNear(x, y, z), RANGE_GOAL)
                except:
                    bot.chat("Can't find that")
            if message.startswith('go to player'):
                try:
                    targetplayer = message.split('player')[1].strip()
                    player = bot.players[targetplayer]
                    target = player.entity
                    if not target:
                        bot.chat("Can't find a clear path!")
                        return
                    pos = target.position
                    bot.pathfinder.setMovements(movements)
                    bot.pathfinder.setGoal(pathfinder.goals.GoalNear(
                        pos.x, pos.y, pos.z), RANGE_GOAL)
                except:
                    bot.chat("Can't find that")
            if message.startswith('add target'):
                try:
                    targetlist.append(message.split('target')[1].strip())
                    print(targetlist)
                except:
                    bot.chat('Error')
            if message.startswith('distance'):
                player = bot.players[sender]
                entity = player.entity
                if not entity:
                    bot.chat('Can\'t measure that far')
                    return
                try:
                    pos = bot.entity.position
                    print(pos)
                    distance = bot.players[sender].entity.position.distanceTo(
                        pos)
                    bot.chat(distance)
                    return
                except:
                    bot.chat('error')
            if message.startswith('shut down'):
                if sender and (sender == CMDR):
                    bot.chat('Shutting down...')
                    bot.quit('Shutting down...')


@On(bot, 'physicTick')
def handle(*args):
    nearby = [[], []]
    pos = bot.entity.position
    try:
        for name in targetlist:
            targetplayer = bot.players[name]
            nearby[0].append(targetplayer.username)
            targetentity = targetplayer.entity
            if not targetentity:
                return
            distance = bot.players[name].entity.position.distanceTo(pos)
            nearby[1].append(distance)
    except:
        return
    try:
        closest_distance = min(nearby[1])
        nearby_index = nearby[1].index(closest_distance)
        closest_player = nearby[0][nearby_index]
        target = bot.players[closest_player]
        try:
            print('a')
            bot.pvp.attack(target.entity)
        except:
            print('b')
            return
    except:
        return


@On(bot, "end")
def handle(*args):
    print("Bot ended!", args)
