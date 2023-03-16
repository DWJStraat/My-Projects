const mineflayer = require('mineflayer')

import config from './config.json.example' assert { type : 'JSON' }
import newxp from './new_xp.json' assert { type : 'JSON' }

const bot = mineflayer.createBot(
    host = config.host,
    port = config.port,
    username = config.username,
    auth = config.auth
)

bot.on('spawn', () => {
    console.log('spawned, commencing xp update')
    for (const [key, value] of Object.entries(newxp)){
        console.log(key +':' + value)
    }
})
