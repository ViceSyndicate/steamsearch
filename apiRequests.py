import requests
import json
import time

class Game:
    def __init__(self, name, ID, platforms, genres, short_Description):
        self.name = name
        self.ID = ID
        self.platforms = platforms
        self.genres = genres
        self.short_Description = short_Description

steamGamesUrl = 'http://api.steampowered.com/ISteamApps/GetAppList/v2/'
steamGameIds = []
steamGameReviewScore = 'https://store.steampowered.com/appreviews/{id}?json=1'

#def getRequest(url):

def getRequest(url):
    request = requests.get(url)
    if request.status_code != 200:
        print('GET ' + url + ' Failed!')
        print('returning empty string...')
        return ''
    else:
        print('Success! Returning Content...')
        gamesData = json.loads(request.content)
        return gamesData

    #jsonData = json.loads(jsonGames.content)
    #return jsonData

def getGameList():
    jsonData = getRequest(steamGamesUrl)
    return jsonData['applist']['apps']

def returnMatchingGameIds(sheetGames, steamGames):
    # For every gameName in sheetGames
    for sheetName in sheetGames:
        #print(sheetName)
        # Check every gameName in steamGames
        for game in steamGames:
            # if a steamGame has a title matching our list of games
            # Add that games appid to our steamGamesId list
            if game['name'] == sheetName:
                #print(game['name'])
                #print(sheetName)
                if not steamGameIds.__contains__(game['appid']):
                    steamGameIds.append(game['appid'])
                else:
                    print("couldn't find " + game['name'])
    return steamGameIds

def getAppData(id):
    url = "https://store.steampowered.com/api/appdetails?appids=" + str(id)
    jsonGame = requests.get(url)
    jsonData = json.loads(jsonGame.content)
    success = jsonData[str(id)]['success']
    gameData = {}
    if (success):
        name = jsonData[str(id)]['data']['name']

        #loop through each item in generes and get description
        genres_data  = jsonData[str(id)]['data']['genres']
        gameGenres = [genre['description'] for genre in genres_data]
        #platforms = jsonData[str(id)]['data']['platforms']

        platforms = []
        platformData = jsonData[str(id)]['data']['platforms']
        # {'windows': True, 'mac': True, 'linux': False}
        for platform, value in platformData.items():
            # if the platform is true: add it to list of platforms.
            # platforms ex: "windows": true, "mac": true,"linux": false
            if value:
                platforms.append(platform)

        short_Description = jsonData[str(id)]['data']['short_description']
        time.sleep(2.5)
        reviewScore = getReviewData(id)

        gameData = {
            "name": name,
            "id": id,
            "platforms": platforms,
            "genres": gameGenres,
            "reviewScore": reviewScore,
            "short_Description": short_Description
        }
        return gameData
        
    else:
        print("couldn't get appdetails!")
    #return jsonData[str(id)]['applist']['apps']

    # Rating, Platform, description(Single/Multiplayer capabilities) and Tags. 
def getReviewData(id): 
    url = 'https://store.steampowered.com/appreviews/' + str(id) + '?json=1'
    review_score = ''
    jsonGame = requests.get(url)
    jsonData = json.loads(jsonGame.content)
    if (jsonData['success']):
        review_score = jsonData['query_summary']['review_score_desc']
    else:
        print("Couldn't get appreview data")
    return review_score

# Rating, Platform, description(Single/Multiplayer capabilities) and Tags. 

# TODO 
# Fill google sheet fields with the data that we DID find.