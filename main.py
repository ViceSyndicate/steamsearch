import gspread

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
    gameList = worksheet.col_values(2)

    counter = 1
    for val in gameList:

        print(str(counter) + ' - ' + val)
        counter = counter +1
    
    # TODO Make steam api search on each title in gameList
    # get Rating, Platform and Tags. 
    # Store them in lists OR
    # Create a object for each game that has each variable in it. 
    # Update sheet columns 2, 3 and 4 with those values for each game.
    
    print('------------')
    pause = input("Press Enter to continue")

if __name__ == "__main__":
    main()
