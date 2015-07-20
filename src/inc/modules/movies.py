'''Search movie titles and get ratings, release year, simple plot.
intended for an irc bot, but can be used where ever.
Author: techb - nulldigit
Date: July 18 2015

Needs tested with actual bot, getMovieInfo() is confirmed working though.'''

import json
import urllib
from inc import *

modFunc.addCommand('movie', 'movies', 'movies')

def getMovieInfo(title):
    titlesplit = title.lower().strip().split() #oh may lol
    # if the movie title is more than one word,
    # join it so the url can use it, else just nothing
    if len(titlesplit) > 1:
        newtitle = "+".join(titlesplit)
    else:
        newtitle = titlesplit[0]
        
    url = "http://www.omdbapi.com/?t=%s&plot=short&r=json" % newtitle
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    if data['Response'] == 'True':
        return ("Title: "+data['Title'],
                "Year: "+data['Year'],
                "Rating: "+data['imdbRating'],
                "Plot: "+data['Plot'])
    else:
        return (False, "Movie: %s not found, check spelling?" % title)
    
def movies(line, irc):
    splitline = line.split(" :")
    message, whole, username, msgto = ircFunc.ircMessage(line.strip(), whl=True)
    movie_title = whole.strip()
    if msgto.lower() == configFunc.getBotConf('nickname').lower():
        msgto = username
    msg2 = message[1].lower()
    if msg2.strip():
        ircFunc.ircSay(msgto, "Fetching...", irc)
        data = getMovieInfo(movie_title)
        if data[0] != False:
            for info in data:
                ircFunc.ircSay(msgto, info, irc)
        else:
            ircFunc.ircSay(msgto, data[1], irc)
