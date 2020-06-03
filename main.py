import os
import re
import secrets

import discord

client = discord.Client()

dnd_regex = re.compile(r'^\d*d\d+$')

def dnd(expr):
    sentences = expr.replace(' ', '').split(',')
    results = []
    for s in sentences:
        processes = s.split('+')
        result = 0
        dices = []
        for p in processes:
            match = dnd_regex.match(p)
            if match:
                factors = p.split('d')
                n = int(factors[0])
                dice = int(factors[1])
                for t in range(0, n):
                    r = secrets.randbelow(dice) + 1
                    dices.append(r)
                    result += r + 1
            else:
                result += int(p)
        results.append((dices, result))
    reply = '\n'.join([f'{x[0]}={x[1]}' for x in results])
    return reply


def awaken(expr):
    sentences = expr.replace(' ', '').split(',')
    results = []
    for s in sentences:
        dices = []
        n = int(s)
        s = 0
        f = 0
        for t in range(0, n):
            r = secrets.randbelow(6) + 1
            dices.append(r)
            if r >= 5:
                s += 1
            elif r <= 2:
                f += 1
        results.append((dices, (s, f)))

    def calc_result(tup):
        if tup[0] > 0:
            return f'{tup[0]} S'
        else:
            return f'{tup[1]} F'

    reply = '\n'.join([f'{x[0]}=({calc_result(x[1])})' for x in results])
    return reply


flags = {
    '!dnd': dnd,
    '!awa': awaken
}

# results = dnd('2d20 + 2, 1d20 + 1')
# reply = awaken('2, 1')
# print(reply)
# 1/0

@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for flag in flags:
        if message.content.startswith(flag):
            reply = ''

            try:
                expr = message.content[len(flag) + 1:]
                reply = flags[flag](expr)
                reply = f'{message.author.name} rolou:\n{reply}'
            except Exception:
                reply = 'Hum... deu ruim, tenta mandar algo tipo !dnd 1d20 + 2 ou !awa 5'

            await message.channel.send(reply)
    return

client.run(os.environ.get('TOKEN', ''))
