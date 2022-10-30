### imports
# Acces to gmail
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import random
import pandas as pd
from collections import defaultdict

# voice
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice").Speak

# open collins dictionary in case of error
import webbrowser

# for the wrong answers
import datetime


def googleDocReadIn():
    ### Read-in google doc
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] # link of my google sheet

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('szotar-362715-b509492797b1.json', scope) # json file contains my own key

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('DICTIONARY / SZOTAR') # name of the spreadsheat file
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
    records_df.columns = ["skip", "word", "meaning", "type", "help", "word freq", "counter"]
    records_df = records_df.iloc[1:]
    ### old: 
    '''words_array = records_df["word"].to_numpy()
    meaning_array = records_df["meaning"].to_numpy()
    help_array = records_df["help"].to_numpy()'''
    ### new:
    words_array = list(records_df["word"])
    meaning_array = list(records_df["meaning"])
    help_array = list(records_df["help"])
    
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
    return records_df, wordsStat, words_array, meaning_array, stats_data, stat, help_array
 
 # fill in empty cells, to avoid further problems
 ## could be done in the read in function, but anyway
def emptyCellsHandler(words_array, meaning_array, help_array):
    meaning_array_n, help_array_n = [],[]
    for w,m,h in zip(words_array, meaning_array, help_array):
        if m == "" or m == "?":
            meaning_array_n.append("no saved meaning of: "+w)
        else:
            meaning_array_n.append(m)
        if h == "":
            help_array_n.append("no saved help of: "+w)
        else:
            help_array_n.append(h)
            
    return meaning_array_n, help_array_n


 
def questions(words_array, meaning_array, help_array, numbersQuiz, length=1):
    # quizNumbers = random.choices(list(set(numbersQuiz)), k=length) # this is wrong, gives back duplicated values. 
    # just for fun, random shuffle twice! 
    random.shuffle(numbersQuiz)
    random.shuffle(numbersQuiz)
    quizNumbers = numbersQuiz[0:length]
    quizQ = []
    remainMeanings = meaning_array.copy()
    # remainMeanings = remainMeanings.tolist()
    # print("INFO: Length of the meaning array ", len(remainMeanings))
    #print("INFO: SET of the meaning array ", len(set(remainMeanings)))
    #print("INFO: ",quizNumbers)
    
    for i in quizNumbers:
        #print(words_array[i], meaning_array[i])
        # print(i, " -" ,meaning_array[i])
        quizQ.append([words_array[i],meaning_array[i], help_array[i]])
        remainMeanings.remove(meaning_array[i])
    return quizQ, remainMeanings
    
    
def deleteKnownWords(wordsStat, words_array, meaning_array, help_array, days=31):
    wordStatDict = defaultdict(list)
    # we need a set to built up the default dictionary
    wordStatSet = set(wordsStat["Word"])
    timestamp = datetime.datetime.now().timestamp()
    last30Years = 9460800
    numberOfGoodAnswersInaRow = 5
    for i in wordStatSet:
        wordStatDict[i] = []
    for i,row in wordsStat.iterrows():
        # for OK
        try:
            n = int(row["OK"])
            wordStatDict[row["Word"]].append(n)
        except:
            None
        # for NOK
        try:
            n = int(row["NOK"])
            wordStatDict[row["Word"]].append(-n)
        except:
            None
    knownWords = []        
    # get rid of known words
    # if the last three element average is older than now()+2 month, delete it from the set 
    #print(wordStatSet)
    for i in wordStatSet:
        # since the dates are continiously appended we dont have to sort them. 
        check = sum(wordStatDict[i][-3:])/3
        #print(i)
        if check+(62*24*3600)>timestamp:
            # print("Known word ## ", i)
            knownWords.append(i)
            
        # if the 
        # var = wordStatDict[i]
        #check = sum(wordStatDict[i][-5:])/5
        
        """
        check = (sum(var[-numberOfGoodAnswersInaRow:]))/numberOfGoodAnswersInaRow
        if i == "d":
            print(check <  timestamp)
            print(len(var[-numberOfGoodAnswersInaRow:]) >= numberOfGoodAnswersInaRow)
            print(sum(wordStatDict[i][-numberOfGoodAnswersInaRow:]), check, timestamp, )
        #check = mean(var[-numberOfGoodAnswersInaRow:])
        if (len(var[-numberOfGoodAnswersInaRow:]) >= numberOfGoodAnswersInaRow) & (check <  timestamp):
            print(i)
            print(check >  timestamp)
            print("*** WTFS ****")
            print(sum(wordStatDict[i][-numberOfGoodAnswersInaRow:]), check, timestamp, )
            """
    
    
            
    words_array_n, meaning_array_n, help_array_n = words_array.copy(), meaning_array.copy(), help_array.copy()
    numberOfKnownWords = 0
    for w, m, h in zip(words_array, meaning_array, help_array):
        if w in knownWords:
            #words_array.remove(w)
            #meaning_array(m)
            #print(w)
            words_array_n.remove(w)
            meaning_array_n.remove(m)
            help_array_n.remove(h)
            
            numberOfKnownWords += 1
    
    print("Number of known words: ",  numberOfKnownWords, "\n Number of unknown words: ", len(words_array)-numberOfKnownWords)   
    numbersQuiz = list(range(0, len(words_array_n)))
    # print("Number of quiz is : ", numbersQuiz)
            
    return words_array_n, meaning_array_n, help_array_n, numbersQuiz
    
# user input validator
def userInputValidator(maxN):
    ''' Validate user input '''
    while True:
        try:
            number = int(input())
            if number < 1 or number > maxN:
                raise ValueError #this will send it to the print message and back to the input option
            break
        except ValueError:
            print("Invalid input or too big number. Try it again")
    return number