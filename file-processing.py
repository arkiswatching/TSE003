#fair warning, this is not great, it'll run more on document similarity than anything else

def core():
  #needed to function   
  import nltk
  from nltk.stem import WordNetLemmatizer
  #downloads packages if not present
  nltk.download('popular', quiet=True)

  #file opening, might need adusting depending on file input type, need the actual file to refine
  qnafile=open('qnafile.txt','r')
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
