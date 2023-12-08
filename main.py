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
    
    # TODO Get all ID's in list.
    # Fill in that row with data using ID.
    #sheetGameIdList = worksheet.col_values(1)[1:]
    
    steamGames = apiRequests.getGameList()
    matchingIds = apiRequests.returnMatchingGameIds(sheetGameList, steamGames)
    #matchingIds = matchingIds[:10]
    print('matching game names: '+str(len(matchingIds))+'/'+str(len(sheetGameList)))
    

    gameDataList = []

    newsheet = spreadsheet.worksheet('Copy of Copy of Keys for Giveaway')
    headers = ['id', 'Name', 'Platforms', 'Popular User Defined Tags', 'Steam All-time Review Score %']
    newsheet.insert_rows([headers], 1)
    data_to_insert = []

    GetGamesFromIds(worksheet)

    for id in matchingIds:
        # wait to avoid spamming steams api 
        # and getting timed out/blocked.
        #time.sleep(1)
        print('Requesting data on ID: ' + str(id))
        
        # this can return NoneType if bad ID is sent in 
        game = apiRequests.getAppData(id)
        print(game)
        #TODO Check if game is NoneType
        print("----------")
        if game is not None and game['Name'] is not None: 
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
                if name == game['Name']: #TODO OR id in sheetGameList == game['id']
                    # Update the corresponding cells in the Google Sheet
                    row_number = sheetGameList.index(name) + 2  # Adding 2 to convert to sheet row number
                    worksheet.update_cell(row_number, 1, game['id'])
                    time.sleep(1)
                    worksheet.update_cell(row_number, 7, game['Steam All-time Review Score %'])
                    time.sleep(1)
                    worksheet.update_cell(row_number, 8, ', '.join(game['Platforms']))
                    time.sleep(1)
                    worksheet.update_cell(row_number, 9, game['Singleplayer/Multiplayer Capabilities']) # single/multiplayer
                    time.sleep(1)
                    worksheet.update_cell(row_number, 10, ', '.join(game['Popular User Defined Tags']))
                    # Add more updates as needed
                    break

    print('------------')
    print('Finished!')
    pause = input("Press Enter to continue")

def GetGamesFromIds(worksheet):
    
    # get all values in column A except for the title column.
    sheetIdList = worksheet.col_values(1)[1:]
    # sheedIdList looks like this: ['793460', '', '',...]
    for index, id in enumerate(sheetIdList, start=2):

        # if the id value for column is empty. skip updating.
        if id == '':
            continue

        print("id: " + id)
        # get data to fill in row cells
        game = apiRequests.getAppData(id)
        row_number = sheetIdList.index(id) + 2
        
        worksheet.update_cell(row_number, 1, game['id'])
        time.sleep(1)
        worksheet.update_cell(row_number, 2, game['Name'])
        time.sleep(1)
        worksheet.update_cell(row_number, 7, game['Steam All-time Review Score %'])
        time.sleep(1)
        worksheet.update_cell(row_number, 8, ', '.join(game['Platforms']))
        time.sleep(1)
        worksheet.update_cell(row_number, 9, game['Singleplayer/Multiplayer Capabilities']) # single/multiplayer
        time.sleep(1)
        worksheet.update_cell(row_number, 10, ', '.join(game['Popular User Defined Tags']))
        # Add more updates as needed
        break

if __name__ == "__main__":
    main()

