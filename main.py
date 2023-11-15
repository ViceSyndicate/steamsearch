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
    sheetGameList = worksheet.col_values(2)
    #remove the first value which is the name of the column.
    sheetGameList.pop(0)

    
    
    
    
    steamGames = apiRequests.getGameList()
    matchingIds = apiRequests.returnMatchingGameIds(sheetGameList, steamGames)
    matchingIds = matchingIds[:2]
    print('matchingames: '+str(len(matchingIds))+'/'+str(len(sheetGameList)))
    

    gameDataList = []

    
    for id in matchingIds:
        # wait 2.5s to avoid spamming steams api 
        # and getting timed out/blocked.
        time.sleep(2.5)
        print('Requesting data on ID: ' + str(id))
        gameDataList.append(apiRequests.getAppData(id))
    
    for game in gameDataList:
        print(game)
    
    newsheet = spreadsheet.worksheet('Copy of Copy of Keys for Giveaway')
    headers = ['id', 'Name', 'Platforms', 'Popular User Defined Tags', 'Steam All-time Review Score %']
    newsheet.insert_rows([headers], 1)
    data_to_insert = []
    for game in gameDataList:
            # Extract the attributes from the Game object
            row_data = [
            game['id'],
            game['Name'],
            ', '.join(game['Platforms']),
            ', '.join(game['Popular User Defined Tags']),
            game['Steam All-time Review Score %'],
            #game['Popular User Defined Tags']
            ]
            data_to_insert.append(row_data)
        
    for game in gameDataList: 
         print(game)


    newsheet.insert_rows(data_to_insert, 2)
    
    #reviewCol = 'F'

    #colPos = 1
    #sheetNames = worksheet.col_values(2)

    
    #worksheet.append_row(values=platformList, table_range='H2')

    print('------------')
    pause = input("Press Enter to continue")

if __name__ == "__main__":
    main()


    '''
    # Specify the CSV file name
    csv_filename = "games.csv"

    
    # Open the CSV file for writing
    with open(csv_filename, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)

        # Write the header row (if needed)
        header = ["Name", "ID", "Platforms", "Genres", "Description"]
        csv_writer.writerow(header)

        # Write data for each Game object in the list
        for game in gameDataList:
            # Extract the attributes from the Game object
            row_data = [
            game['name'],
            game['id'],
            ', '.join(game['platforms']),
            ', '.join(game['genres']),
            game['short_Description']
            ]

            # Write the row to the CSV file
            csv_writer.writerow(row_data)

        print(f"Data has been written to {csv_filename}")
    '''


    '''
    for sheetName in sheetNames:
        print(str(colPos) + '-' + sheetName)
        colPos = colPos +1
        for game in gameDataList:
            if game['name'] == sheetName:
                reviewCol + str(colPos)
                worksheet.update(range_name=reviewCol, values=game['reviewScore'])
            reviewCol = 'F'
    '''     
        
    '''
    for game in sheetGameList:
        worksheet.col_values()
        game['name']
        game['platforms']
        colPos+1
    '''