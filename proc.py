import nltk
import spacy


# nltk.download('stopwords')
# nltk.download('punkt')

# nlp = spacy.load("en_core_web_sm")

stop_words = set(nltk.corpus.stopwords.words('english'))

text = "NLTK is a powerful library for natural language processing."
# doc = nlp(text)
# print(doc)

tokens = nltk.word_tokenize(text.lower())

filtered_text = [word for word in tokens if word not in stop_words or not word.isalpha()]

print(filtered_text)