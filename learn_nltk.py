import nltk

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk


# tokenization
text = "NLTK is a leading platform for building Python programs to work with human language data."
words = word_tokenize(text)
sentences = sent_tokenize(text)

print("Words:", words)
print("Sentences:", sentences)

# remove stop words
stop_words = set(stopwords.words('english'))
filtered_words = [word for word in words if word.lower() not in stop_words]

print("Filtered Words:", filtered_words)

# stemming
stemmer = PorterStemmer()
stemmed_words = [stemmer.stem(word) for word in filtered_words]

print("Stemmed Words:", stemmed_words)

# lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

print("Lemmatized Words:", lemmatized_words)

# part-of-speech tagging
nltk.download('averaged_perceptron_tagger_eng')
tagged_words = nltk.pos_tag(words)

print("POS Tagged Words:", tagged_words)


# Named Entity Recognition
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')
ner_tree = ne_chunk(tagged_words)

print("Named Entities:", ner_tree)