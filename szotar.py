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

### INIT
# define the number of questions 
numberOfQuestions = 5
numberWrongAnswers = 1

# user inputs
print(" How many words? ")
numberOfQuestions = int(input())
print(" how many possible answers? ")
numberWrongAnswers = int(input())

####################### INIT
### Read-in google doc

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('szotar-362715-b509492797b1.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('DICTIONARY / SZOTAR')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get all the records of the data
records_data = sheet_instance.get_values()
# delete empty records
while(['', '', '', '', '#N/A'] in records_data):
    records_data.remove(['', '', '', '', '#N/A'])
    
# get the records, invert it, etc
records_df = pd.DataFrame.from_dict(records_data)
records_df.columns = ["word", "meaning", "type", "help", "counter"]
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

######################## INIT END

quizNumbers = random.choices(numbersQuiz, k=numberOfQuestions)

def questions(words_array, meaning_array, numbersQuiz, length=numberOfQuestions):
    quizNumbers = random.choices(numbersQuiz, k=numberOfQuestions)
    quizQ = []
    remainMeanings = meaning_array.copy()
    remainMeanings = remainMeanings.tolist()
    for i in quizNumbers:
        #print(words_array[i], meaning_array[i])
        quizQ.append([words_array[i],meaning_array[i]])
        remainMeanings.remove(meaning_array[i])
    return quizQ, remainMeanings
    
quizQ, possibleWrongAnswers = questions(words_array, meaning_array, numbersQuiz)

def quizF (quizQ, possibleWrongAnswers,numberWrongAnswers):
    for i in quizQ:
        question = i[0]
        goodAnswer = i[1]
        # define x wrong answer
        #11print("-------- quizF ", question, goodAnswer)
        wrongAnswers = random.choices(possibleWrongAnswers, k=numberWrongAnswers)
        mapAnswers(question, goodAnswer, wrongAnswers, numberWrongAnswers)
        # print(question, goodAnswer, " ::: wrong ones ::: ", wrongAnswers)
        
def mapAnswers(question, goodAnswer, wrongAnswers, numberWrongAnswers):
    q = []
    q.append(goodAnswer)
    dicT = {}
    #print("Q: ", question, " A: ", goodAnswer)
    ######## until here it is good
    for i in wrongAnswers:
        q.append(i)
    random.shuffle(q)
    #print("## q is this: ", q)
    n = range(1,numberWrongAnswers+2)
    ######## until here it is goodŰ
    for n, a in zip(n, q):
        dicT[n] = a
    
    answeringF(dicT,goodAnswer, question)
    return 0
    
def answeringF(dicT, goodAnswer, question):
    print(question)
    # say it
    speak(question)
    
    # print the answers
    for i in dicT:
        print(i," - ", dicT[i])
    try:
        ans = int(input())
    except KeyError:
        print("::: again:::: ")
    if dicT[ans] == goodAnswer:
        print("Good answer! ")
        print("--------------")
        goodAnswersDict[question] = int(datetime.datetime.now().timestamp())
    else:
        # wrong answer
        wrongAnswersDict[question] = int(datetime.datetime.now().timestamp())
        print("Correct answer: ", goodAnswer)
        webbrowser.open('https://www.collinsdictionary.com/dictionary/english/'+question)
        # print("::: MAPPED GOOD ANSWER IS: ", )
        # print(" ::: DICT :::: ", dicT)
        
# decleare an empty viaraible for the wrong answers
wrongAnswersDict = {}
goodAnswersDict = {}

quizF(quizQ, possibleWrongAnswers, numberWrongAnswers)

# append wrong and good answers
for i in wrongAnswersDict:
    wordsStat = wordsStat.append({'Word': i, "NOK":wrongAnswersDict[i], "OK":"" }, ignore_index=True)
for i in goodAnswersDict:
    wordsStat = wordsStat.append({'Word': i, "OK":goodAnswersDict[i], "NOK":"" }, ignore_index=True)

# update the sheet
stat.update([wordsStat.columns.values.tolist()] + wordsStat.values.tolist())

print("Type something to exit")
int(input())