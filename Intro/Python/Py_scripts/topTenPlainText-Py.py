import sys
import os
sys.path.insert(0,"/N/u/cyberdh/Carbonate/dhPyEnviron/lib/python3.6/site-packages")
os.environ["NLTK_DATA"] = "/N/u/cyberdh/Carbonate/dhPyEnviron/nltk_data"

          
from nltk.corpus import stopwords
import os
import string
from collections import defaultdict
import operator
import matplotlib.pyplot as plt
import numpy as np
import re
import math


homePath = os.environ['HOME']
dataHome = os.path.join(homePath, 'Text-Analysis-DavidBranchV2', 'data', 'shakespeareFolger')
dataResults = os.path.join(homePath, 'Text-Analysis-DavidBranchV2', 'Output')

singleDoc = False
nltkStop = True
customStop = True
stopWords = []

# NLTK Stop words
if nltkStop is True:
    stopWords.extend(stopwords.words('english'))

    stopWords.extend(['would', 'said', 'says', 'also', 'good', 'lord', 'come'])

#print(" ".join(stopwords.fileids()))

if customStop is True:
    stopWordsFilepath = os.path.join(homePath, "IntroTextAnalysis", "data", "earlyModernStopword.txt")

    with open(stopWordsFilepath, "r",encoding = 'utf-8') as stopfile:
        stopWordsCustom = [x.strip() for x in stopfile.readlines()]

    stopWords.extend(stopWordsCustom)
    
def textClean(text):
    
    text = text.strip().lower()
    
    tokens = re.split(r'\W+', text)
    
    # remove empty string
    tokens = [t for t in tokens if t]
    
    # remove digits
    tokens = [t for t in tokens if not t.isdigit()]
    
    # built-in stop words list
    tokens = [t for t in tokens if t not in stopWords]
        
    # remove punctuation
    puncts = list(string.punctuation)
    puncts.append('--')

    tokens = [t for t in tokens if t not in puncts]

    return tokens


    
"""
Get sorted frequency in descending order
"""
def getFreq(tokens):
    
    freq = defaultdict(int)

    for t in tokens:
        freq[t] += 1
    
    # sorted frequency in descending order
    return sorted(freq.items(), key = operator.itemgetter(1), reverse = True)

def plotTopTen(sortedFreq, title, imgFilepath, dpi):
    
    topn = 15

    for t in sortedFreq[0 : topn]:
        
        print('{} : {}'.format(t[0], t[1]))
    
    topNWords = [w for w in sortedFreq[0 : topn]]

    x_pos = np.arange(len(topNWords))
    cnts = [w[1] for w in topNWords]

    plt.rcdefaults()

    plt.bar(x_pos, cnts, align = 'center', alpha = 0.5, color = ['red', 
                                                             'orange', 'yellow', 'green', 'blue',
                                                             'darkorchid', 'darkred', 'darkorange', 
                                                             'gold', 'darkgreen'])
    

        
    plt.xticks(x_pos, [w[0] for w in topNWords])
    plt.xticks(rotation = 45)
        
    xlabel = plt.xlabel('Words')
    xlabel.set_color('red')
    ylabel = plt.ylabel('Frequency')
    ylabel.set_color('red')
    
    high = max(cnts)
    low = 0
    
    plt.ylim(low, math.ceil(high + 0.1 * (high - low)))
    
    for xpos, count in zip(x_pos, cnts):
    
        plt.text(x = xpos, y = count + 1, s = str(count), ha = 'center', va = 'bottom')

    plt.title(title)
 
    plt.savefig(imgFilepath, format = 'png', dpi = dpi, bbox_inches = 'tight')
    
    plt.show()
    
    
def getTokensFromSingleText(textFilepath):
    
    with open(textFilepath, "r", encoding = 'utf-8') as f:
        text = f.read()

    return textClean(text)


def getTokensFromScan(corpusRoot):
    
    tokens = []
    
    for root, subdirs, files in os.walk(corpusRoot):
        
        for filename in files:
            
            # skip hidden file
            if filename.startswith('.'):
                continue
            
            textFilepath = os.path.join(root, filename)
            
            with open(textFilepath, "r", encoding = "utf-8") as f:
                text = f.read()
                tokens.extend(textClean(text))
                
                print('Finished tokenizing text {}\n'.format(textFilepath))
    
    return tokens


if singleDoc is True:
    # Use case one, analyze top 10 most frequent words from a single text

    textFilepath = os.path.join(dataHome, 'Hamlet.txt')

    # get tokens
    tokens = getTokensFromSingleText(textFilepath)

    # get frequency
    freq = getFreq(tokens)

    title = 'Top 10 Words, Hamlet'

    imgFilepath = os.path.join(dataResults, 'hamletTopTenPlainText.png')

    dpi = 300

    plotTopTen(freq, title, imgFilepath, dpi)
else:
    # Use case two, analyze top 10 most frequent words from a corpus root

    tokens = getTokensFromScan(dataHome)

    # get frequency
    freq = getFreq(tokens)

    title = 'Top 10 Words, Shakespeare'

    imgFilepath = os.path.join(dataResults, 'starTrekTopTenPlainText.png')

    dpi = 300

    plotTopTen(freq, title, imgFilepath, dpi)
