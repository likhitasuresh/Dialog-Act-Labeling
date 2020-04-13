# **Dialog Act Labeling using pycrfsuite**

## **Aim**
This project aims at utilizing pycrfsuite to label utterances with corresponding dialog acts.

## **Experiment**
The training set of around 900 CSV files with dialogues were provided to the crfsuite model. 

## Baseline features included:
* Marker if speakers changed between utterances
* Feature for every token in the utterance
* Feature for every token's POS tag in the utterance

In order to increase accuracy, an advanced feature list with the following features was used:
* Token for every consecutive pair of words
* Token for commonly occuring letter pairs such as "th", "he", "in"

The accuracy % increase noticed was 1.3%.

## Tool source
* https://pypi.org/project/python-crfsuite/
* https://nbviewer.jupyter.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb
* http://www.chokkan.org/software/crfsuite/
