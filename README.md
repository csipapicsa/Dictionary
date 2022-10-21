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
  
- Date of the good/wrong answers are recorded in the same google sheet (for todo)


#### Other
- It opens when computer is switched on
  - can be automatize for timeperiods (open every hours, etc)


### TODO:
#### Soon
  - Check whenever sound card is available 
	- If is not, skip to use it
  - Don't add the words to the teaching list, which has 6 good hit in a row
  - Don't show the pandas append bullshit message in the end
#### Later on   
  - After a help sentence arises add NOK to the statistics
  - Handle if the sheet is not available (no internet, make local copy, etc)
	- Version control? Differencies between two dataframe? Local copy vs cloud. 
  
  tags: google sheet, python, dictionary, word teacher, learning
