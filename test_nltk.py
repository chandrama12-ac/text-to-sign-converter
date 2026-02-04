import nltk
import os

print(f"NLTK Data path: {nltk.data.path}")

try:
    print("Testing tokenization...")
    tokens = nltk.word_tokenize("Success is a journey")
    print(f"Tokens: {tokens}")
except LookupError:
    print("FAIL: Tokenizer data missing")
except Exception as e:
    print(f"FAIL: Tokenizer error: {e}")

try:
    print("Testing POS tagging...")
    tags = nltk.pos_tag(["Success", "is", "test"])
    print(f"Tags: {tags}")
except LookupError:
    print("FAIL: POS tagger data missing")
except Exception as e:
    print(f"FAIL: POS tagger error: {e}")

try:
    print("Testing Lemmatization...")
    from nltk.stem import WordNetLemmatizer
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize("running", pos='v')
    print(f"Lemma: {lemma}")
except LookupError:
    print("FAIL: WordNet data missing")
except Exception as e:
    print(f"FAIL: Lemmatizer error: {e}")
