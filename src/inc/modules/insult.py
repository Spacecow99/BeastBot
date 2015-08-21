'''
Insult a user.
'''

import random
from inc import *

modFunc.addCommand('insult', 'insult', 'insult')

# TODO: extend.
nouns = [
    'fucker',
    'ass',
    'motherfucker',
    'asshole',
    'idiot',
    'skid',
    'lardass',
    'piece of shit',
    'dumb fuck',
    'retard',
    'skid',
]

# TODO: extend.
adjectives = [
    'lazy',
    'dumb',
    'skiddish',
    'proprietary'
]

# TODO: extend.
phrases = [
    'Shut up, {NICK}, you {adj} {noun}!',
    'Eat shit, {NICK}!',
    'Why are you so {adj}, {NICK}, maybe you\'re just a {noun}?',
    'You are such a little {noun} {NICK}.',
    'Why be a {adj} {noun}, {NICK}?',
    '{NICK}, you {adj} {noun}.'
]


def build_phrase(nick):
    p = random.choice(phrases)
    while '{' in p:
        rep = p[p.index('{'):p.index('}')+1]
        if rep == '{NICK}':
            p = p.replace(rep, nick)
        elif rep == '{adj}':
            p = p.replace(rep, random.choice(adjectives))
        elif rep == '{noun}':
            p = p.replace(rep, random.choice(nouns))
    return p


def insult(line, irc):
    message, username, msgto = ircFunc.ircMessage(line)
    if message[1]:
        nick = message[1].strip()  # not sure about that, document your API!
        ircFunc.ircSay(msgto, build_phrase(nick), irc)
