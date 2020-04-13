# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:45:35 2020

@author: Likhita Suresh
"""

import pycrfsuite
import hw2_corpus_tools as tools
import os, sys


#getting path to train date - appending train data file to current path
#path = os.getcwd()+"\\trainSmall"
inputDir = sys.argv[1]
testDir = sys.argv[2]
outputFile = sys.argv[3]


#print (path)




#print (csv_data[0][0][2][0].token)
csv_data = list(tools.get_data(inputDir))


#feature for every token
def tokenFeatures (wordList):
    tokens = []          
    for i in range(len(wordList)):
        tokens.append('TOKEN_'+wordList[i].token)
    return tokens

#feature for every pos
def posFeatures (wordList):
    tags = []    
    for word in wordList:        
        tags.append('POS_'+word.pos)
    return tags

#feature for every sentence
def sentFeatures (dialogue, i):    
    
    act = dialogue[i][0]
    speaker = dialogue[i][1]    
    wordList = dialogue[i][2]    
    sent_features = []
       
    if(i>0):
        if(dialogue[i][1]!=dialogue[i-1][1]):                    
            sent_features.append('SPEAKER_CHANGED')
    if(i==0):
        sent_features.append('first')
    
    if wordList is None:
        sent_features.append("NO_WORDS")
    else:
        sent_features.extend(tokenFeatures(wordList))
        sent_features.extend(posFeatures(wordList))   

    return sent_features

#fetching label for a sentence
def sentLabels(sent):    
    return sent[0]


#gathering features for given dataset
def features(inputDir):
    features = []
    labels = []
    #getting data from given directory as list 
    csv_data = list(tools.get_data(inputDir))
    for dialogue in csv_data:      
        dialogue_features = [] 
        dialogue_labels = []
        for i in range(len(dialogue)):                 
            #dialogue_features.append(sentFeatures(dialogue,i))
            #dialogue_labels.append(sentLabels(dialogue[i]))
            features.append(sentFeatures(dialogue,i))
            labels.append(sentLabels(dialogue[i]))
        #features.append(dialogue_features)
        #labels.append(dialogue_labels)
    return features, labels, csv_data

#training model
trainResults = features(inputDir)
X_train = trainResults[0]
y_train = trainResults[1]

testResults = features(testDir)
X_test = testResults[0]
y_test = testResults[1]
dialogues = testResults[2]

trainer = pycrfsuite.Trainer(verbose=False)

trainer.append(X_train,y_train)    

#features = 

trainer.set_params({
'c1': 1.0, # coefficient for L1 penalty
'c2': 1e-3, # coefficient for L2 penalty
'max_iterations': 50, # stop earlier
# include transitions that are possible, but not observed
'feature.possible_transitions': True
})



trainer.train('80strain.crfsuite')

tagger = pycrfsuite.Tagger()
tagger.open('80strain.crfsuite')

y_pred = tagger.tag(X_test)
output_labels = ""
for i in range(len(dialogues)):
    for j in range(len(dialogues[i])):
        output_labels += y_pred[j]+"\n"
    output_labels += "\n"
    
f = open(outputFile, "w")
f.write(output_labels)

correct = 0
for i in range(len(y_test)):
    if(y_pred[i]==y_test[i]):
        correct = correct+1
accuracy = correct/len(y_test)