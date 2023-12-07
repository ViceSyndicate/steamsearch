import requests
import json
import time
import math

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
            # ALT?: if game['name'].__contains__(sheetName):
            
            if game['name'] == sheetName: # to compare 'id' we would need to send a list of ID's in too..
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

        platforms = []
        platformData = jsonData[str(id)]['data']['platforms']
        # {'windows': True, 'mac': True, 'linux': False}
        for platform, value in platformData.items():
            # if the platform is true: add it to list of platforms.
            # platforms ex: "windows": true, "mac": true,"linux": false
            if value:
                platforms.append(platform)

        short_Description = jsonData[str(id)]['data']['short_description']
        time.sleep(1)

        '''
        reviewScore = ''
        try: 
            reviewScore = jsonData[str(id)]['data']['metacritic']['score']
            reviewScore = str(reviewScore) + '%'
        except KeyError:
            print("metacritic score does not exist. Getting steam review instead.")
            reviewScore = getReviewData(id)
        '''

        reviewScore = getReviewData(id)
        singleMultiplayerData = ''
        categories = jsonData[str(id)]['data']['categories']
        for category in categories:
            if category['description'] == "Single-player" or category['description'] == "Multi-player" or category['description'] == "Online Co-op":
                # add category['description'] to list to then remove the last ", "
                singleMultiplayerData += category['description'] + ", "
        #TODO don't add ", " if it's the last result in descriptions 

        gameData = {
            "id": id,
            "Name": name,
            "Platforms": platforms,
            "Popular User Defined Tags": gameGenres,
            "Steam All-time Review Score %": reviewScore,
            "Singleplayer/Multiplayer Capabilities": singleMultiplayerData
            #"short description": short_Description
        }
        return gameData
        
    else:
        print("couldn't get appdetails for ID: " + str(id))

    # Rating, Platform, description(Single/Multiplayer capabilities) and Tags. 
    # gets steam page review data instead of metacritics% review.
def getReviewData(id): 
    url = 'https://store.steampowered.com/appreviews/' + str(id) + '?json=1&language=all'
    #https://store.steampowered.com/appreviews/934780?json=1&language=all
    review_score = ''
    jsonGame = requests.get(url)
    jsonData = json.loads(jsonGame.content)
    if (jsonData['success']):
        #review_score = jsonData['query_summary']['review_score_desc']
        totalPositiveReviews = jsonData['query_summary']['total_positive']
        totalReviews = jsonData['query_summary']['total_reviews']

        if(totalReviews == 0):
            reviewPercentege = ''
        else:
            sum = math.floor((totalPositiveReviews / totalReviews) * 100)
            reviewPercentege = str(sum) + '%'

        
        #print("dividing " + str(totalPositiveReviews) + ' / ' + str(totalReviews))
        #print(totalPositiveReviews / totalReviews)
        #print("Multiplying by 100 = " + str(sum))
        

    else:
        print("Couldn't get appreview data")
    return reviewPercentege

# Rating, Platform, description(Single/Multiplayer capabilities) and Tags. 
