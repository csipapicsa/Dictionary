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
records_df, wordsStat, words_array, meaning_array, numbersQuiz, stats_data, stat, help_array = m.wordsSheet(sheet)

# make quiz
quizQ, possibleWrongAnswers = m.questions(words_array, meaning_array, help_array, numbersQuiz, length=numberOfQuestions)

def quizF (quizQ, possibleWrongAnswers,numberWrongAnswers):
    for i in quizQ:
        question = i[0]
        goodAnswer = i[1]
        helP = i[2]
        # define x wrong answer
        # print("-------- quizF ", question, goodAnswer)
        wrongAnswers = m.random.choices(possibleWrongAnswers, k=numberWrongAnswers)
        mapAnswers(question, goodAnswer, helP, wrongAnswers, numberWrongAnswers)
        # print(question, goodAnswer, " ::: wrong ones ::: ", wrongAnswers)
        
def mapAnswers(question, goodAnswer, helP, wrongAnswers, numberWrongAnswers):
    q = [] #variable for all answers
    q.append(goodAnswer)
    dicT = {}
    # print("Q: ", question, " A: ", goodAnswer, " H: ", helP)
    ######## until here it is good
    for i in wrongAnswers:
        q.append(i)
    m.random.shuffle(q)
    #print("## q is this: ", q)
    n = range(1,numberWrongAnswers+2)
    ######## until here it is good
    for n, a in zip(n, q):
        # n=number, a=corresponding answer
        # print(n, "  ", a)
        dicT[n] = a
    
    answeringF(dicT,goodAnswer, helP, question) ### unlock it after the help is done
    return None


def goodAnswerDictWrite(question):
    print("Good answer! ")
    print("--------------")
    goodAnswersDict[question] = int(m.datetime.datetime.now().timestamp())
    return 

def goodAnswerChecker(dicT, ans, goodAnswer):
    if dicT[ans] == goodAnswer:
        return True
    else:
        return False
    
def answeringF(dicT, goodAnswer, helP, question):
    print(question)
    # say it
    m.speak(question)
    # print(helP)
    # print the answers
    for i in dicT:
        print(i," - ", dicT[i])
    try:
        ans = int(input())
    except KeyError:
        print("::: again:::: ")
    if goodAnswerChecker(dicT, ans, goodAnswer): #if the answer is good
        goodAnswerDictWrite(question)
    else:
        # wrong answer, print help
        print("### Wrong answer, help: ", helP)
        ans = int(input())
        if goodAnswerChecker(dicT, ans, goodAnswer):
            goodAnswerDictWrite(question)
        if goodAnswerChecker(dicT, ans, goodAnswer) == False:
            wrongAnswersDict[question] = int(m.datetime.datetime.now().timestamp())
            print("Correct answer: ", goodAnswer)
            m.webbrowser.open('https://www.collinsdictionary.com/dictionary/english/'+question)
            # print("::: MAPPED GOOD ANSWER IS: ", )
            # print(" ::: DICT :::: ", dicT)
                
###################################

# decleare an empty viaraible for the wrong answers
wrongAnswersDict = {}
goodAnswersDict = {}

quizF(quizQ, possibleWrongAnswers, numberWrongAnswers)
print("### Write stat in the sheet")
# append wrong and good answers
for i in wrongAnswersDict:
    wordsStat = wordsStat.append({'Word': i, "NOK":wrongAnswersDict[i], "OK":"" }, ignore_index=True)
for i in goodAnswersDict:
    wordsStat = wordsStat.append({'Word': i, "OK":goodAnswersDict[i], "NOK":"" }, ignore_index=True)

# update the sheet
stat.update([wordsStat.columns.values.tolist()] + wordsStat.values.tolist())

print("### Write DONE")