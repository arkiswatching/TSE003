# trys to import packages, on error they are downloaded then imported
try:
    import pandas as pd
    import numpy as np
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pandas'])
finally:
    import pandas as pd
    import numpy as np
try:
    import nltk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'nltk'])
finally:
    import nltk
try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'sklearn'])
finally:
    import sklearn
import os
import subprocess
import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer # to perform tfidf
from sklearn.metrics import pairwise_distances # to perform cosine similarity
from nltk.stem import wordnet # to perform lemmitization
from nltk import pos_tag # for parts of speech
from nltk import word_tokenize # to create tokens
from nltk.corpus import stopwords # for stop words (needs integrating)


def text_normalisation(text):
    text=str(text).lower() # text to lower case
    spl_char_text=re.sub(r'[^ a-z]','',text) # removing special characters
    tokens=nltk.word_tokenize(spl_char_text) # word tokenizing
    lema=wordnet.WordNetLemmatizer() # intializing lemmatization
    tags_list=pos_tag(tokens,tagset=None) # parts of speech
    lema_words=[] # empty list
    for token,pos_token in tags_list:
        if pos_token.startswith('V'): #verbs
            pos_val= 'v'
        elif pos_token.startswith('J'): #Adjective
            pos_val='a'
        elif pos_token.startswith('R'): #adverb
            pos_val= 'r'
        else:
            pos_val= 'n' # noun
        lema_token=lema.lemmatize(token,pos_val) # performing lemmatization
        lema_words.append(lema_token) # appending the lematized token into lists
    return " ".join(lema_words) # returns the lematized token into sentences


def chat():
    print("LiBot: Hello! I'm LiBot, a chatbot created to help you with any questions you may have regarding the University of Lincoln's library. Press the 'esc' key if you wish to exit.")
    loop = True
    while loop == True:
        user_input = input('User: ')
        normalised_input = text_normalisation(user_input)

        tfidf = TfidfVectorizer() # initialises vectorizor
        df_tfidf = tfidf.fit_transform(df['Normalised Context']).toarray() # vectorizing context into array
        input_tfidf = tfidf.transform([normalised_input]).toarray() # vectorizing input into array
        cos_sim = 1 - pairwise_distances(df_tfidf,input_tfidf,metric = 'cosine') # performs cosine similarity between vectoried data and input
        index = cos_sim.argmax() # finds largest similarity value

        if cos_sim[index] < 0.4:
            print("liBot: Sorry, I didn't understand that.")
        else:
            print("LiBot: " + df['Response'].loc[index])


file_dir = os.path.dirname(os.path.abspath(__file__)) # assigns file directory to a variable
df = pd.read_excel(file_dir + "\Library_Knowledge_Base.xlsx", usecols = ['Context', 'Response']) # reads excel file
df.ffill(axis = 0, inplace = True) # fills 'NaN' cells
df['Normalised Context'] = df['Context'].apply(text_normalisation) # creates normalised column using a function


chat()
