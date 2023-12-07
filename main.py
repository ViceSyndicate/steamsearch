import gspread
import apiRequests
import time
import csv

def main():
    print("Executing...")
    print('------------')
    # do authentification for google spreadsheets
    gc = gspread.service_account(filename='credentials.json')
    gc.auth
    #get testspreadsheet
    spreadsheet = gc.open("DEV COPY Tsumi's Giveaway Games")
    #get working sheet
    worksheet = spreadsheet.worksheet('Copy of Keys for Giveaway')
    #get all values from column 1
    sheetGameList = worksheet.col_values(2)[1:]
    #sheetIdList = worksheet.col_values(1)[1:]
    
    # TODO Get all ID's in list.
    # Fill in that row with data using ID.
    #sheetGameIdList = worksheet.col_values(1)[1:]
    
    steamGames = apiRequests.getGameList()
    matchingIds = apiRequests.returnMatchingGameIds(sheetGameList, steamGames)
    #matchingIds = matchingIds[:10]
    print('matchingames: '+str(len(matchingIds))+'/'+str(len(sheetGameList)))
    

    gameDataList = []

    for id in matchingIds:
        # wait to avoid spamming steams api 
        # and getting timed out/blocked.
        time.sleep(1)
        print('Requesting data on ID: ' + str(id))
        gameDataList.append(apiRequests.getAppData(id))
    
    newsheet = spreadsheet.worksheet('Copy of Copy of Keys for Giveaway')
    headers = ['id', 'Name', 'Platforms', 'Popular User Defined Tags', 'Steam All-time Review Score %']
    newsheet.insert_rows([headers], 1)
    data_to_insert = []

    #keysToCheck = ["id", "Name", "Platforms", "Popular User Defined Tags", "Steam All-time Review Score %"]
    #for key in keysToCheck:

    # we could move this loop in to matchingIds loop? 

    for game in gameDataList:
            # Extract the attributes from the Game object
            print(game)
            print("----------")
            if game['Name'] is not None: 
                row_data = [
                game['id'],
                game['Name'],
                ', '.join(game['Platforms']),
                ', '.join(game['Popular User Defined Tags']),
                game['Steam All-time Review Score %'],
                #game['Popular User Defined Tags']
                ]
                data_to_insert.append(row_data)
    
    for name in sheetGameList:
        for game_data in gameDataList:
            if name == game_data['Name']:
                # Update the corresponding cells in the Google Sheet
                row_number = sheetGameList.index(name) + 2  # Adding 2 to convert to sheet row number
                worksheet.update_cell(row_number, 1, game_data['id'])
                time.sleep(1)
                worksheet.update_cell(row_number, 7, game_data['Steam All-time Review Score %'])
                time.sleep(1)
                worksheet.update_cell(row_number, 8, ', '.join(game_data['Platforms']))
                time.sleep(1)
                worksheet.update_cell(row_number, 9, game_data['Singleplayer/Multiplayer Capabilities']) # single/multiplayer
                time.sleep(1)
                worksheet.update_cell(row_number, 10, ', '.join(game_data['Popular User Defined Tags']))
                # Add more updates as needed
                time.sleep(1)
                break

    print('------------')
    print('Finished!')
    pause = input("Press Enter to continue")

if __name__ == "__main__":
    main()

