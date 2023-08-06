import numpy as np
import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer 
wn_lemmatiser = WordNetLemmatizer()

def tokenise(sentence):
  tokens = ''.join([char if ord('a') <= ord(char.lower()) <= ord('z') or char == "'" or char.isdigit() else ' ' for char in f'{sentence} '.replace(':','').replace("`","'").replace('pm ',' pm ')])
  ts = []
  for token in tokens.split():
    if "am " in f'{token} ' and len(token) > 2 and token[-3].isdigit(): #avoid splitting words like ham, spam, sam, etc
      ts.extend([token[:-2],"am"])
    else:
      ts.append(token)
  return ts

def normalise(sentence): 
  return ["*" * len(token) if token.isdigit() else wn_lemmatiser.lemmatize(token.lower(),'v') for token in tokenise(sentence)]  

def one_hot(matrix, n_classes):  
  vector = np.zeros((np.array(matrix).shape[0], n_classes))
  for i,vs in enumerate(matrix):
    vector[i][vs] = 1.
  return vector

def wordvectors(file_path):
  vectors = {}
  with open(file_path) as f:
    for line in f.readlines():
      line = line.split()
      word,vector = line[0],np.array(line[1:],dtype='float32')
      vectors[word] = vector
  return vectors

def embeddingmatrix(wordvectors,vector_length,vocabulary):
  matrix = np.zeros((2+len(vocabulary),vector_length))
  for word,idx in vocabulary.items():
    if word.lower() in wordvectors:
      matrix[idx] = wordvectors[word.lower()]
  return matrix

def clip_pad(xs,length,pad=[0]):
  xs = [x[:length] for x in xs]  #clips it if too long
  xs = [x + pad * (length - len(x)) for x in xs] #pads it if too short
  return xs

def preprocess(sentence, model_info):
  ts = [model_info["word_vocab"][token] if token in model_info["word_vocab"] else 1 for token in normalise(sentence)]
  ts = clip_pad([ts],model_info["sentence_length"])
  cs = [[model_info["char_vocab"][char] if char in model_info["char_vocab"] else 1 for char in token] for token in tokenise(sentence)]
  cs = clip_pad([clip_pad(cs,model_info["word_length"])],model_info["sentence_length"],pad=[[0]*model_info["word_length"]])
  return [ts,cs]

def postprocess(model_output, model_info):
  ii,ee = model_output
  intents = [model_info["intent_idx"][i] for i in ii.argmax(1)]
  entities = [model_info["entity_idx"][e] if e in model_info["entity_idx"] else None for e in ee.argmax(2)[0]]
  return intents,entities

def intent_entities(sentence,model,model_info): #wrapper: -> input string -> output intents & entities
  intent,entities = postprocess(model.predict(preprocess(sentence,model_info)),model_info) 
  return intent, list(zip(tokenise(sentence),entities))
