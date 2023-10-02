import gspread

def main():
    print("Executing...")
    print('------------')
    # get get authentification for spreadsheets
    gc = gspread.service_account(filename='credentials.json')
    gc.auth
    #get testspreadsheet
    spreadsheet = gc.open('TestSheet')
    #get working sheet
    worksheet = spreadsheet.worksheet('Sheet1')
    #get all values from column 1
    gameList = worksheet.col_values(1)

    for val in gameList:
        print(val)
    
    # TODO do steam api search on each title in gameList
    # get Rating, Tags and store them for each game.
    # Update sheet columns 2 and 3 with those values. 
    
    print('------------')
    searchQuery = input("Press Enter to continue")

if __name__ == "__main__":
    main()
