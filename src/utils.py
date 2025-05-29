import spacy
from transformers import pipeline

nlp = spacy.load('en_core_web_sm')

def clean_text(texto):
    doc = nlp(texto.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def sentiment_classifier(text, clean=False):
    classifier = pipeline("sentiment-analysis")
    if len(text) > 512:
        raise Exception("The lenght of string is to long, max characters is 512")
    
    if clean:
        clean_text(text)
    
    return classifier(text)