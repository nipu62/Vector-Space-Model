"""
Created on Sat Sep 25 12:06:29 2021
@author: Ayesha Siddika Nipu
Description: This program will read contents from Sonnets.txt file and count words for each sonnet. The sonnet number and word counts will be stored in a dictionary. Then the mean, median and standard deviations are calculated using the python statistics module.
"""

import string
import statistics

filename = "Sonnets.txt"
myDict = {}
sonnet_no = []

def readlines(fname):
    """Return contents of file as a list of strings"""
    f = open(fname, 'r')  #Open file for reading
    lines = f.readlines()       #Read contents as a list of strings
    lines = [line.rstrip() for line in lines] #removes \n from each line
    f.close()   #Return file resources to the operating system
    return lines

def remove_punc(s):
    '''Returns string s with the punctuation removed'''
    res = ["".join( j for j in i if j not in string.punctuation) for i in  s]
    return s

def has_numbers(inputString):
    '''Returns true/falsed whether any number is found in a line or not'''
    return any(char.isdigit() for char in inputString)
 
def getFirstSonnetNumber(docWithoutPunc):
    '''Returns the first sonnet number of the document.'''
    for lines in docWithoutPunc:
        if has_numbers(lines.strip()):
            return lines.strip()
        
    return ''
    
def getDictWithWordCount(allLines):
    '''Returns a dictionary with the words count for each sonnet'''
    count = 0
    last_sonnet_no = getFirstSonnetNumber(allLines)
    #Return if no number tag is found for sonnet in a file
    if(len(last_sonnet_no) == 0):
        return {}
    for current_line in allLines:
        if has_numbers(current_line) == True:
            current_sonnet_no = current_line.strip()
            #print ("dictionary doesn't have this key\n")
            myDict[last_sonnet_no] = count
            myDict[current_sonnet_no] = 0
            last_sonnet_no = current_sonnet_no
            count = 0
                
        else:
            if myDict:
                if len(current_line.strip())>0:
                    count += len(current_line.split())
                    #print(count)
                    
    myDict[last_sonnet_no] = count
    return myDict
    
def main():
    readDoc = readlines(filename)
    docWithoutPunc = remove_punc(readDoc)
    word_count_dict = getDictWithWordCount(docWithoutPunc)
    #print(word_count_dict)
    if word_count_dict:
        print("\n Dictionary [Sonnet Number, Word Count]","\n\n", word_count_dict, "\n")
        mean_val = statistics.mean(word_count_dict.values())
        
        print("Mean : ", round(mean_val, 1), "\n")  
    
        median_val = statistics.median(word_count_dict.values())
        print("Median : ", round(median_val), "\n")        
        
        stdev_val = statistics.stdev(word_count_dict.values())
        print("Standard deviation : ", round(stdev_val, 1), "\n") 
        
         
    else:
        print("Invalid document! Please provide a correct one.")
                            
    #print(docWithoutPunc)
    
if __name__ == "__main__":
    main()
