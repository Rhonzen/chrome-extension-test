from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import json 
import csv

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
token_length = 4

def getTitle(text):
    prompt = 'Generate a Title for this: '
    #prompt = 'What is the main argument made in this news article? Be detailed in your response. Seperate arguments by '
    #print(len(tokenizer(prompt + text).input_ids))
    if len(tokenizer(prompt + text).input_ids) > 2000:
        print('summarised again')
        text = summarize(text, 0.2)
        
    input_text = prompt + '\n' + text
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_length=100)
    outputs = tokenizer.decode(outputs[0])[6:-4]
    
    return [outputs]

def summarize(text, per):
    nlp = spacy.load('en_core_web_lg')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

import os
from os.path import join, getsize
sets = []
header = ['Post', 'Url', 'Real', 'Title', 'Claims']
with open('claims_real.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for root, dirs, files in os.walk("."):
        for name in files:
            print(os.path.join(root, name))
            sets.append(name)
	
            if "real" in root:
                m = open(os.path.join(root, name))
                loaded = json.load(m)
                text = loaded['text']
                url = loaded['url']
                post = root[20:]
                l = len(text)
                if l == 0: 
                    continue
                per = 200/l
                res = summarize(text, per)
                while (len(res) < 10):
                    per = per * 2
                    if per > 1:
                        per = 1
                    res = summarize(text, per)
                    if per == 1:
                        break
                title = getTitle(text)
                res = res.split('\n') 
                res = [value for value in res if value != '']
                res = ["|" + r + "|" for r in res]
                if "real" in root:
                    real = 1
                else:
                    real = 0
                data = [post, url, real, title, res]
                print(post)
                writer.writerow(data)

    
    