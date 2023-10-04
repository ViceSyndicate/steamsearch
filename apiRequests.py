import requests
import json

steamGamesUrl = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
steamGameReviewScore = 'https://store.steampowered.com/appreviews/{id}?json=1'

def getGameList():
    jsonGames = requests.get(steamGamesUrl)
    jsonData = json.loads(jsonGames.content)
    return jsonData['applist']['apps']

def compareGameLists():
    print('WIP')