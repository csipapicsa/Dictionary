### imports
# Acces to gmail
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import random
import pandas as pd
# voice
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice").Speak

# open collins dictionary in case of error
import webbrowser


# for the wrong answers
import datetime


def hell(x):
	print(x+111)
	return 111

def googleDocReadIn():
    ### Read-in google doc

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('szotar-362715-b509492797b1.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('DICTIONARY / SZOTAR')
    return sheet
    
def wordsSheet(sheet):
    # get the first sheet values, turn them into pandas df, clean the empty rpws
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    # get all the records of the data
    records_data = sheet_instance.get_values()
    #    delete skippable and empty records
    records_data_new = []
    for elem  in records_data:
        if elem[1] == "" or elem[0] == "TRUE":
            None
        else:
            records_data_new.append(elem)

    
    # get the records, invert it, etc
    records_df = pd.DataFrame.from_dict(records_data_new)
    records_df.columns = ["skip", "word", "meaning", "type", "help", "counter"]
    records_df = records_df.iloc[1:]
    words_array = records_df["word"].to_numpy()
    meaning_array = records_df["meaning"].to_numpy()
    # create numbers
    numbersQuiz = list(range(0, words_array.size))
    # check the length of the array than pick up 3 random samples

    #### STAT READ IN
    stat = sheet.get_worksheet(1)
    stats_data = stat.get_values()
    # delete what we dont need
    while(['', '', ''] in stats_data):
        stats_data.remove(['', '', ''])
    # import it pandas DF
    wordsStat = pd.DataFrame(stats_data, columns = ["Word", "OK", "NOK"])
    wordsStat = wordsStat.iloc[1:,:] # delete first row
    return records_df, wordsStat, words_array, meaning_array, numbersQuiz, stats_data, stat