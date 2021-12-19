"""
Created on Sun Nov 21 13:00:32 2021

@author: Ayesha Siddika Nipu (an37s)
"""
import os
import string
import re
import math
import time
import operator
from nltk.corpus import stopwords
from collections import defaultdict
import nltk as tk
tk.download('stopwords')

fileLabelName = "file_label.txt"
fileQueryName = "query.txt"

docFreqDict = {}
docLabelDict = {}
contentDict = {}
ctDict = {}
rsvDict = {}

# Folder Path
path = os.path.abspath(os.getcwd()) + '\\documents'
os.chdir(path)
stop_words = set(stopwords.words('english')) 
uniqueWordFreqDict = defaultdict(lambda: 0)

N = len([name for name in os.listdir(path) if name.startswith('file_') and os.path.isfile(name)])

def ConvertAndShowElapsedTime(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    print('Elapsed Time: {:.2f} hr {:.2f} min {:.2f} sec'.format(h, m, s)) # Python 3
    #return str(datetime.timedelta(sec))

def readlines(filename):
    mypath = os.getcwd() + "\\"+ filename
    """Return contents of file as a list of strings"""
    f = open(mypath, 'r')  
    lines = f.readlines()       
    lines = [line.rstrip() for line in lines] 
    f.close()   
    return lines

def DataPreprocessing(sen):
    text_string = sen.lower()
    str_without_num = re.sub(r'\d+', '', text_string)
    str_without_punc = str_without_num.translate(str.maketrans('', '', string.punctuation))
    toks = tk. word_tokenize ( str_without_punc )
    stemmer = tk. stem . PorterStemmer ()
    stemmed_words = [ stemmer . stem ( word ) for word in toks ]
    filtered_sentence = [w for w in stemmed_words if not w. lower () in stop_words ]
    return filtered_sentence

def GetUniqueWordsFrequency(filtered_sentence):
    for item in filtered_sentence:
        if item in filtered_sentence:
            uniqueWordFreqDict[item] += 1
        else:
            uniqueWordFreqDict[item] = 1
            
def GetQueryFromFile():
    query = readlines(fileQueryName)
    global queryList
    queryList = DataPreprocessing(query[0])

def GetContentsForEachDoc():
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            fileno = filename_without_ext.split("_")[1]    
            with open(file_path, 'r') as f:
                document_text = f.read()
                filtered_sentence = DataPreprocessing(document_text)
                contentDict[int(fileno)] = filtered_sentence    
                
def GetDocumentFrequency():
    for word, freq in uniqueWordFreqDict.items():
        count = 0
        for key, val in contentDict.items():
            if word in val:
                count += 1
        docFreqDict[word] = count
    
def GetLabelsForEachDoc():
    labels = readlines(fileLabelName)
    for each in labels:
        splittedTxt = each.split(",")
        filename = splittedTxt[0]
        filename_int = int(filename.split("_")[1])
        label = splittedTxt[1]
        docLabelDict[filename_int] = label
    
def GetRelevantExistNotExistCount(term):
    relExistCount = 0
    relNotExistCount = 0
    for doc, label in docLabelDict.items():
        if int(label) == 1:
            if term in contentDict[doc]:
                relExistCount += 1
            else:
                relNotExistCount += 1
    return relExistCount, relNotExistCount        

def calculateCt(s, S, dft):
    numerator = (s+0.5)/(S-s+0.5)
    denominator = (dft-s+0.5)/(N-dft-S+s+0.5)
    Ct = round(math.log10(numerator/denominator),2)
    return Ct
    
    
def CalculateCtForEachTerm():
    for term in queryList:
        relAndExist, relAndNotExist = GetRelevantExistNotExistCount(term)
        small_S = relAndExist
        capital_S = relAndNotExist + small_S
        if term in docFreqDict:
            df_t = docFreqDict[term]
        else:
            df_t = 0
            
        res = calculateCt(small_S, capital_S, df_t)
        ctDict[term] = res
    
def CalculateRSVForEachDoc():
    for i in range(1, N+1):
        rsv = 0
        for term in queryList:
            if term in contentDict[i]:
                rsv += ctDict[term]
        rsvDict[i] = rsv
    
def GetTopTenDocumentWithHighRSV():
    print()
    print('The top 10 documents with high RSV: \n')
    res = sorted(rsvDict.items(), key=operator.itemgetter(1), reverse = True)
    res_dict = dict(res)
    counter = 0;
    for key, val in res_dict.items():
        if counter < 10:
            print('\tRSV{file_' + str(key).ljust(5) + '} = '.ljust(8), str(val).ljust(10), '\tLabel: ', docLabelDict[key])
            counter += 1
            if counter >= N:
                break
        else:
            break
    print()          
                
def main():
    start = time.time()
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                document_text = f.read()
                filtered_sentence = DataPreprocessing(document_text)
                GetUniqueWordsFrequency(filtered_sentence)
    GetContentsForEachDoc()
    GetDocumentFrequency()
    os.chdir("..")
    GetLabelsForEachDoc()
    GetQueryFromFile()
    CalculateCtForEachTerm()
    CalculateRSVForEachDoc()
    GetTopTenDocumentWithHighRSV()
    
    end = time.time()
    ConvertAndShowElapsedTime(end - start)
    
if __name__ == "__main__":
    main()