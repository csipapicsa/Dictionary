#### imnport
import main as m
import importlib as r
# get the sheets
print("*** get the sheet")
sheet = m.googleDocReadIn()
# user inputs - how many questions, how many possible answers
print(" How many words? ")
numberOfQuestions = int(input())
print(" how many possible answers? ")
numberWrongAnswers = int(input())
print("*** making the quiz")
records_df, wordsStat, words_array, meaning_array, numbersQuiz, stats_data, stat = m.wordsSheet(sheet)

def questions(words_array, meaning_array, numbersQuiz, length=numberOfQuestions):
    quizNumbers = m.random.choices(numbersQuiz, k=numberOfQuestions)
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
        wrongAnswers = m.random.choices(possibleWrongAnswers, k=numberWrongAnswers)
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
    m.random.shuffle(q)
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
    m.speak(question)
    
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
        goodAnswersDict[question] = int(m.datetime.datetime.now().timestamp())
    else:
        # wrong answer
        wrongAnswersDict[question] = int(m.datetime.datetime.now().timestamp())
        print("Correct answer: ", goodAnswer)
        m.webbrowser.open('https://www.collinsdictionary.com/dictionary/english/'+question)
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