#NORMALISATION IMPLEMENTATION

#IMPORTING NECESSARY LIBRARIES (If libaries are already installed then delete these)
import pandas as pd 
import nltk
import numpy as np
import re
from nltk.stem import wordnet # to perform lemmitization
from sklearn.feature_extraction.text import CountVectorizer # to perform bow
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf
from nltk import pos_tag # for parts of speech
from sklearn.metrics import pairwise_distances # to perform cosine similarity
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words

#IMPORTING QnA Data SET INTO PANDAS DATA FRAME

df= pd.read_excel('Library_Knowledge_Base.xlsx')
df.head()

df.shape[0] # returns number of rows within data set

#Null values are presented to provide a stuatory response for similiar groups of qs.

df.ffil(axis = 0,inplace=True) # fills null value with previous values
df.head(5)

##############################################################
## FIRST STEP OF NORMALISATION
## CONVERT DATA INTO LOWER CASE AND REMOVE SPECIAL CHARACTER

df1=df.head(10) # copies first ten rows of dataset

#function that converts text into lower case and removes special characters

def step1(x0:
          for i in x:
          a=str(i).lower()
          p=re.sub(r'[^a-z0-9]','',a)
          print(p)

step1(df1['Context'])

## WORD TOKENIZING IS THE PROCESS OF CONVERTING TEXT STRINGS INTO TOKENS LIST, ie split sentences into words

##word tokenizing
s= 'Are you doing alright'
words=word_tokenize(s)
print(words)

## pos_tag funciton returns parts of speech for each token.
##lemmatizer function would then detect these and convert the token into root words
    

pos_tag(nltk.word_tokenize(s),tagset = None) # returns parts of speach for each word

## THEN PERFORM LEMMATIZATION

lemma = wordnet.WordNetLemmatizer() # intializing lemmatizer
lemma.lemmatize('absorbed', pos = 'v')

##IMPLEMENTATION OF NORMALISATION

def text_normalisation(text):
    text=str(text).lower() # text to lower case
    spl_char_text=re.sub(r'[^ a-z]','',text) #removing special characters
    tokens=nltk.word_tokenize(spl_char_text) # word tokenizing
    lema=wordnet.WordNetLemmatizer() #intializing lemmatization
    tages_list=pos_tag(tokens,tagset=None)#parts of speech
    lema_words=[] # empty list
    for token,pos_token in tags_list:
        if post_token.startswith('V'): #verbs
            pos_val= 'v'
        elif pos_token.startswith('J'): #Adjective
            pos_val='a'
        elif pos_token.startswith('R'); #adverb
        pos_val= 'r'
        else:
            pos_val= 'n' # noun
            lema_token=lema.lemmatize(token,pos_val) # performing lemmatization
            lema_words.append(lema_token) # appending the lematized token into lists
    return " ".join(lema_words) # returns the lematized token into sentences

##NOW APPLYING THE FUNCTION INTO DATASET

text_normalization('You have been helpful') #will normalise the text for the chatbot to recognise as You've been helpful

df['lemmatized_text']=df['Context'].apply(text_normalization) # applying the function to dataset to clean text
df.head()

##Bow (bag of words)

# bag of words

cv = CountVectorizer() #intializing count vecotrizer
X = cv.fit_transgorm(df['lemmatized_text']).toarray()

#then returns all unique words from data

features = cv.get_feature_names()
df_bow = pd.FataFrame(X, columns = features)
df_bow.head()


