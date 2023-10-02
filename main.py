import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    print("Hello World!")
    searchQuery = input("Search: ")

    gc = gspread.service_account()
    
    

if __name__ == "__main__":
    main()
