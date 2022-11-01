# Dictionary
Vocabulary teacher

## How it works?
- Open my google sheet, where are three column: words, meaning and help
- It makes a user defined quiz (number of words, number of wrong answers)
  - The word is spoken via audio
- You need to vote for the good answer

In case of wrong answer:
- you got a help (example sentence from the help column)
- the meaning of the word opens through collins dictionary
  - https://www.collinsdictionary.com/
  



#### Other
- It opens when computer is switched on
  - can be automatize for timeperiods (open every hours, etc)
- Words which has 5 good answeres in a row in the past 1 year are interpreted as known words.


### TODO:
#### Soon
  - Possible answers in alphabetical ascending order (useful in case of big amount of possible answers)
  - Don't show the pandas append bullshit message in the end
#### Later on   
  - After a help sentence arises add NOK to the statistics
  - Handle if the sheet is not available (no internet, make local copy, etc)
	- Version control? Differencies between two dataframe? Local copy vs cloud. 
  
  tags: google sheet, python, dictionary, word teacher, learning
