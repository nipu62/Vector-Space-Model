'''
@Author: Ayesha Siddika Nipu
Description: This program computes similarity creating a vector space model using term frequency, tf-idf, wf-idf for each document.
'''

import os
import nltk as tk
import string
import re
import math 
import time
from nltk.corpus import stopwords
from collections import defaultdict
from scipy import spatial
import operator
from numpy import dot
from numpy.linalg import norm

tk.download('stopwords')
tk.download('punkt')

# Folder Path
path = os.path.abspath(os.getcwd()) + '\\documents'
os.chdir(path)
stop_words = set(stopwords.words('english')) 

uniqueWordFreqDict = defaultdict(lambda: 0)
termFreqDocDict = {}
docFreqDict = {}
inverseDocFreq = {}
tfIdfAllDoc = {}
wfIdfAllDoc = {}

termFreqDictList = {}
tfIdfAllDocDictList = {}
wfIdfAllDocDictList = {}

simUsingTf = {}
simUsingTfIdf = {}
simUsingWfIdf = {}

totalFiles = len([name for name in os.listdir(path) if name.startswith('file_') and os.path.isfile(name)])

def ConvertAndShowElapsedTime(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    print('Elapsed Time: {:.2f} hr {:.2f} min {:.2f} sec'.format(h, m, s)) # Python 3
    #return str(datetime.timedelta(sec))

def StemmingSentence(sen):
    text_string = sen.lower()
    str_without_num = re.sub(r'\d+', '', text_string)
    str_without_punc = str_without_num.translate(str.maketrans('', '', string.punctuation))
    toks = tk. word_tokenize ( str_without_punc )
    stemmer = tk. stem . PorterStemmer ()
    stemmed_words = [ stemmer . stem ( word ) for word in toks ]
    filtered_sentence = [w for w in stemmed_words if not w. lower () in stop_words ]
    return filtered_sentence

def GetCosineSimilarity(list1, list2):
    result = 1 - spatial.distance.cosine(list1, list2)
    return result

def GetCosineSimilarity2(list1, list2):
    cos_sim = dot(list1, list2)/(norm(list1)*norm(list2))
    return cos_sim

def GetTopTenWordsList(uniqueWordFreqDict):
    #print("\nGetTopTenWordsList\n")
    sorted_dict = dict(sorted(uniqueWordFreqDict.items(), key=lambda item: item[1], reverse = True))
    #print(sorted_dict)
    print("The top 10 most frequent words are:")
    i = 1
    for key, val in sorted_dict.items():
        if i <= 10:
            print("\t", i, ". ", key)
            i += 1
        else:
            break

def GetTermFrequencyForEachDoc():
    #print("\nGetTermFrequencyForEachDoc...\n")
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            fileno = filename_without_ext.split("_")[1]    
            with open(file_path, 'r') as f:
                wordFreqDict = {}
                freqList = []
                document_text = f.read()
                #print(document_text)
                filtered_sentence = StemmingSentence(document_text)
                #print("uniqueWordFreqDict", uniqueWordFreqDict)
                for word, freq in uniqueWordFreqDict.items():
                    freq = filtered_sentence.count(word)
                    wordFreqDict[word] = freq
                    freqList.append(freq)
                termFreqDictList[fileno] = freqList
                termFreqDocDict[fileno] = wordFreqDict 
                #print("len = ", len(freqList))
    
    #print("\ntermFreqDictList\n", termFreqDictList)
    #print("\ntermFreqDocDict\n", termFreqDocDict)
    
    
def CalculateSimilarityUsingTF():
    #print("\nCalculateSimilarityUsingTF\n")
    for doc, tf in termFreqDictList.items():
        for i in range (1, totalFiles+1):
            if doc < str(i) and str(i) in termFreqDictList:
                sim = GetCosineSimilarity2(tf, termFreqDictList[str(i)])
                test = doc + '-' + str(i)
                simUsingTf[test] = round(sim, 2)
        #print("\simUsingTfList\n", simUsingTfList)
    
    
def GetDocumentFrequency():
    #print("\nGetDocumentFrequency\n")
    for word, freq in uniqueWordFreqDict.items():
        count = 0
        for key, val in termFreqDocDict.items():
            if val[word] > 0:
                count += 1
        docFreqDict[word] = count
    #print("\ndocFreqDict\n", docFreqDict)
    
def CalculateInverseDocFreq():
    #print("\nCalculateInverseDocFreq\n")
    for word, freq in uniqueWordFreqDict.items():
        val = totalFiles / docFreqDict[word]
        tf_idf = math.log10(val)
        inverseDocFreq[word] = round(tf_idf, 2)
    #print("\ninverseDocFreq\n\n",inverseDocFreq)
    
def CalculateTfIdf():
    #print("\nCalculateTfIdf\n")
    for doc, termFreq in termFreqDocDict.items():
        tfidf = {}
        lst = []
        for term, freq in termFreq.items():
            val = freq * inverseDocFreq[term]
            tfidf[term] = val
            lst.append(val)
        tfIdfAllDocDictList[doc] = lst
        tfIdfAllDoc[doc] = tfidf
        
    #print("\ntfIdfAllDocDictList\n", tfIdfAllDocDictList)
    #print("\ntfIdfAllDoc\n\n", tfIdfAllDoc)
    
def CalculateSimilarityUsingTfIdf():
    #print("\nCalculateSimilarityUsingTfIdf\n")
    for doc, tf in tfIdfAllDocDictList.items():
        #dic = {}
        for i in range (1, totalFiles+1):
            if doc < str(i) and str(i) in tfIdfAllDocDictList:
                sim = GetCosineSimilarity2(tf, tfIdfAllDocDictList[str(i)])
                test = doc + '-' + str(i)
                simUsingTfIdf[test] = round(sim, 2)
    #print("\simUsingTfIdfList\n", simUsingTfIdfList)
    
    
def CalculateWfIdf():
    #print("\nCalculateWfIdf\n")
    for doc, termFreq in termFreqDocDict.items():
        wfidf = {}
        lst = []
        for term, freq in termFreq.items():
            if(freq > 0):
                wf = 1 + round(math.log10(freq), 2)
            else:
                wf = 0
            val = wf * inverseDocFreq[term]
            lst.append(val)
            wfidf[term] = val
            
        wfIdfAllDocDictList[doc] = lst
        wfIdfAllDoc[doc] = wfidf
    #print("\nwfIdfAllDocDictList\n\n", wfIdfAllDocDictList)    
    #print("\nwfIdfAllDoc\n\n", wfIdfAllDoc)
    
    
def CalculateSimilarityUsingWfIdf():
    #print("\nCalculateSimilarityUsingWfIdf\n")
    for doc, tf in wfIdfAllDocDictList.items():
        for i in range (1, totalFiles+1):
            if doc < str(i) and str(i) in termFreqDictList:
                sim = GetCosineSimilarity2(tf, wfIdfAllDocDictList[str(i)])
                test = doc + '-' + str(i)
                simUsingWfIdf[test] = round(sim, 2)
            
    #print("\nsimUsingWfIdf\n", simUsingWfIdf)
    #print("\nsimUsingWfIdfList\n", simUsingWfIdfList)
        

def GetTopClosestDocumentsUsingTf(k): 
    #print("\nGetTopClosestDocumentsUsingTf\n")
    print("\n1. Using tf\n")
    res = sorted(simUsingTf.items(), key=operator.itemgetter(1), reverse = True)
    res_dict = dict(res)
    counter = 0;
    for key, val in res_dict.items():
        if counter < int(k):
            file1 = key.split("-")[0]
            file2 = key.split("-")[1]
            counter += 1
            print("\tfile_" + file1 + ", file_" + file2 + " with similarity of " + str(val))
            print()
        else:
            break

def GetTopClosestDocumentsUsingTfIdf(k): 
    #print("\nGetTopClosestDocumentsUsingTfIdf\n")
    print("\n2. Using tf-idf\n")
    res = sorted(simUsingTfIdf.items(), key=operator.itemgetter(1), reverse = True)
    res_dict = dict(res)
    counter = 0;
    for key, val in res_dict.items():
        if counter < int(k):
            file1 = key.split("-")[0]
            file2 = key.split("-")[1]
            counter += 1
            print("\tfile_" + file1 + ", file_" + file2 + " with similarity of " + str(val))
            print()
        else:
            break
            
            
def GetTopClosestDocumentsUsingWfIdf(k): 
    #print("\nGetTopClosestDocumentsUsingWfIdf\n")
    print("\n3. Using wf-idf\n")
    res = sorted(simUsingWfIdf.items(), key=operator.itemgetter(1), reverse = True)
    res_dict = dict(res)
    counter = 0;
    for key, val in res_dict.items():
        if counter < int(k):
            file1 = key.split("-")[0]
            file2 = key.split("-")[1]
            counter += 1
            print("\tfile_" + file1 + ", file_" + file2 + " with similarity of " + str(val))
            print()
        else:
            break
            
    
def main():
    start = time.time()
    k = input('\nPlease provide the value of k to display the top k closest documents: k = ')
    print("\nTotal number of documents: ", totalFiles)
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                document_text = f.read()
                #print(document_text)
                filtered_sentence = StemmingSentence(document_text)
                #print(filtered_sentence)
                #print()
                for item in filtered_sentence:
                    if item in filtered_sentence:
                        uniqueWordFreqDict[item] += 1

                    else:
                        uniqueWordFreqDict[item] = 1
                        
    #print(myDict)
    print("\nThe number of unique words: ", len(uniqueWordFreqDict.keys()))
    print()
    GetTopTenWordsList(uniqueWordFreqDict)
    
    print("\nCalculating similarity using TF...")
    GetTermFrequencyForEachDoc()
    CalculateSimilarityUsingTF()
    
    print("Calculating similarity using TF-IDF...")
    GetDocumentFrequency()
    CalculateInverseDocFreq()
    CalculateTfIdf()
    CalculateSimilarityUsingTfIdf()
    
    print("Calculating similarity using WF-IDF...")
    CalculateWfIdf()
    CalculateSimilarityUsingWfIdf()
    
    print('\nThe top ' + k + ' closest documents are :\n')
    GetTopClosestDocumentsUsingTf(k)
    GetTopClosestDocumentsUsingTfIdf(k)
    GetTopClosestDocumentsUsingWfIdf(k)
    
    end = time.time()
    ConvertAndShowElapsedTime(end - start)
    
if __name__ == "__main__":
    main()