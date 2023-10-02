import gspread

def main():
    print("Executing...")
    print('------------')
    gc = gspread.service_account(filename='credentials.json')
    gc.auth
    spreadsheet = gc.open('TestSheet')
    worksheet = spreadsheet.worksheet('Sheet1')
    gameList = worksheet.col_values(1)

    for val in gameList:
        print(val)

    print('------------')
    searchQuery = input("Press Enter to continue")

if __name__ == "__main__":
    main()
