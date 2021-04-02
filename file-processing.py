#fair warning, this is not great, it'll run more on document similarity than anything else

def core():
  #needed to function   
  import nltk
  from nltk.stem import WordNetLemmatizer
  #downloads packages if not present
  nltk.download('popular', quiet=True)

  #file opening, might need adusting depending on file input type, need the actual file to refine
  qnafile=open('Library_Knowledge_Base.xlsx','r')
  raw=qnafile.read()
  #converts to lowercase for matching reasons
  raw = raw.lower()

  #convert to list of sentences and take a token score
  sent_tokens = nltk.sent_tokenize(raw)
  #converts to list of words and take a token score
  word_tokens = nltk.word_tokenize(raw)

  #for lemminization, to help match less expertly worded inputs
  lemmed = nltk.stem.WordNetLemmatizer()

  #takes inputs and convets them to the most neutral variant, to further parse down what is being said
  def LemTokens(tokens):
    return [lemmed.lemmatize(token) for token in tokens]
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

  #normalise and remove punctuation from text
  def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
  
  #import to convert raw documents to a matrix of TF-IDF features
  from sklearn.feature_extraction.text import TfidfVectorizer
  
  #import cosine similarity module
  from sklearn.metrics.pairwise import cosine_similarity
  
  #searches users utterace for known keywords and returns one of several responses
  def response(user_response):
    r_response=''
    sent_tokens.append(user_response)
    
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf==0):
        r_response=r_response+"I am sorry! I don't understand you"
        return r_response
    else:
        r_response = r_response+sent_tokens[idx]
        return r_response
   
  #added in for testing but can be altered
  flag=True
  print("BOT: My name is -. I will answer your queries about the University of Lincoln library. If you want to exit, type Bye!")
  while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you'):
            flag=False
            print("BOT: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("BOT: "+greeting(user_response))
            else:
                print("BOT: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("BOT: Bye! take care..")
