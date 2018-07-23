import numpy as np
import pandas as pd
import spacy
import nltk
import dialogflow

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

snowball_stemmer = SnowballStemmer('english')

nlp = spacy.load('en_core_web_sm')


def remove_stopwords(text):
    words = text.split()
    meaningful_words = [w for w in words if w not in stopwords.words("english")]
    return meaningful_words


def text_process(text_input):
    # Remove stopwords
    print(text_input)
    text_input = remove_stopwords(text_input)
    for i, word in enumerate(text_input):
        print(word)
        text_input[i] = snowball_stemmer.stem(word)

    text_input = list(set(text_input))
    print(text_input)

    # Check keywords
    flag1 = False
    for w in text_input:
        if w in ['company', 'packages', 'price']:
            flag1 = True

    if flag1:
        text = respond_packages()
        print(text)

    end_signal = False
    return end_signal


def respond_packages():
    text = 'We provide 5 different career packages, they are:\n'\
            '1. Career Exploration\n'\
            '2. Hybrid Training Satisfaction GUARANTEE\n'\
            '3. 1-Month Resume Success GUARANTEE\n'\
            '4. 3-Month Elite Job Success GUARANTEE\n'\
            '5. 1-Month Sprint to Success GUARANTEE\n'

    return text


def respond_three_month():
    text = 'The 3-Month Elite Job Success GUARANTEE is priced dynamically\n'\
            'Based on the future offer you would get, '

    return text


def main():
    q1 = input("Hi, how can i help you today?")

    program_run = True
    while program_run:  # Run input digest process
        program_run = text_process(q1)


if __name__ == '__main__':
    main()
