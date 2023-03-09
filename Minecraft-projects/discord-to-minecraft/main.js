const {Client, Events, GatewayIntentBits, } = require('discord.js');
GatewayIntentBits.GUILD_MESSAGES = 1 << 9;
GatewayIntentBits.GUILDS = 1 << 0;
GatewayIntentBits.MessageContent = 1 << 15;
const { token, ip, port, username, channel, auth } = require('./config.json');
const mineflayer = require('mineflayer');


const client = new Client({ intents: [GatewayIntentBits.GUILDS, GatewayIntentBits.GUILD_MESSAGES, GatewayIntentBits.MessageContent] });
const bot = mineflayer.createBot({
    host: ip,
    port: port,
    username: username,
    auth: auth
});

client.once(Events.ClientReady, c => {
    console.log(`Ready! Logged in as ${c.user.tag}`);
});

bot.on('chat', (username, message) => {
    if (username === bot.username) return;
    client.channels.cache.get(channel).send(`${username}: ${message}`);
})

client.on('messageCreate', async message => {
    if (message.channelId !== channel) return;
    if (message.author.bot) return;
    bot.chat('!'+message.author.username+'#'+message.author.discriminator+':'+message.content);
});

client.login(token);




