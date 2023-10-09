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

    # TODO Make steam api search on each title in gameList
    # get Rating, Platform and Tags. 
    # Store them in lists OR
    # Create a object for each game that has each variable in it. 
    # Update sheet columns 2, 3 and 4 with those values for each game.

    
    
    
    steamGames = apiRequests.getGameList()
    matchingIds = apiRequests.returnMatchingGameIds(sheetGameList, steamGames)
    
    matchingIds = matchingIds[:5]


    #apiRequests.getAppData(matchingIds[0])
    print('matchingames: '+str(len(matchingIds))+'/'+str(len(sheetGameList)))
    gameDataList = []
    
    for id in matchingIds:
        # wait 2.5s to avoid spamming steams api 
        # and getting timed out/blocked.
        time.sleep(2.5)
        print('Requesting data on ID: ' + str(id))
        gameDataList.append(apiRequests.getAppData(id))
    
    print(gameDataList)
    print(gameDataList[0])

    
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
    
    print('------------')
    pause = input("Press Enter to continue")

if __name__ == "__main__":
    main()
