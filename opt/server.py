#!/usr/bin/env python
# # -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import collections
import dbm
import gensim
import string
import nltk
import copy
import json
import numpy as np
import re
import os
import datetime
import requests as req
from time import sleep
from collections import Counter
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from janome.tokenizer import Tokenizer

cgitb.enable() # デバッグに使うので、本番環境では記述しない

form = cgi.FieldStorage() # フォームデータを取得する

text = form.getvalue("text") # データの値を取得する

def get_text(url, output_file):
    """スクレイピング"""
    try:
        html = req.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        append_text('h1', soup, output_file)
        append_text('p', soup, output_file)
        append_text('h2', soup, output_file)
        append_text('h3', soup, output_file)
        return 
    except:
        return
        
def check_tag(tag, soup):
    """タグのチェック"""
    try:
        texts = soup.find_all(tag)
        return texts
    except:
        return
    
def append_text(tag, soup, output_file):
    texts = check_tag(tag, soup)
    for p in texts:
        output_file.write(p.get_text())

def janome(text, flag):
    """形態素解析"""
    tokenizer = Tokenizer()
    nltk.download('stopwords')
    stopwords_en = stopwords.words('english')
    lines = []
    sentence = str(text)
    tmp = []
    for token in tokenizer.tokenize(sentence):
        pos = token.part_of_speech.split(',')[0]
        if pos in ["名詞", "動詞", "形容詞"]:   # 対象とする品詞
            string = str(token.surface).lower()
            if (not string in stopwords_ja) and string != " " and (not string in stopwords_en):
                tmp.append(string)
    lines.append(tmp)
    return lines

def get_topic_number(corpus, lda):
    """トピックの推定"""
    text = janome(corpus, True)
    dic = gensim.corpora.Dictionary(text)
    corpus = [dic.doc2bow(p) for p in text]
    topics = lda.get_document_topics(corpus, per_word_topics=False)
    save_topic(topics)


def save_topic(topic):
    """トピックの保存"""
    temp = []
    temp2 = []
    topic_num = [[0, i+1] for i in range(50)]
    topic_ls = []
    topic_len = 0
    try:
        for t in topic:
            topic_ls.append(t)
        topic_len = len(topic)
        
    except:
        temp.append(1)
        return

    try:
        for i in range(len(topic_ls)):
            for j in range(len(topic_ls[i])):
                topic_num[topic_ls[i][j][0]][0] += topic_ls[i][j][1]
        for i in topic_num:
            i[0] = i[0]/topic_len
        with open('/cgi-bin/topic.txt', mode='a') as f:
            f.write(str(topic_num))
    except:
        temp2.append(1)
        return

def make_looking(topic_file):
    topic_ls = []
    for i in topic_file.readlines():
        topic_ls.append(i)
    topic_ls = str(topic_ls)

    topic_ls = re.split('\\[|\\]|,', topic_ls)
    topics = []
    for i in range(len(topic_ls)):
        try:
            if float(topic_ls[i]) > 0.01 and float(topic_ls[i+1]):
                print(topic_ls[i], topic_ls[i+1])
                topics.append([topic_ls[i], topic_ls[i+1]])
        except:
            continue
    topics = sorted(topics, reverse=True)
    with open('/actr6/distr-model/param/looking.lisp', mode='w') as f:
        with open('/create-chunk/history/log/topic_log.txt', mode='a') as f2:
            for j in range(3):
                f.write("(set-chunk-slot-value g1-0 looking"+str(j+1)+" l-topic"+topics[j][1]+")\n")
                f2.write("topic:"+topics[j][1]+"\n")


if __name__ == "__main__":
    stopwords_ja = ["し", "い", "よう", "こと", "いる", "あり", "ある", "これ", "さ", "する", "れ",
                "て", "くれる", "やっ", "でき", "ため", "も", "なり"]
    lda = gensim.models.LdaModel.load("/cgi-bin/lda.model")
    with open('/cgi-bin/topic.txt', mode='w') as f:
        f.read
    with open('/cgi-bin/web_text.txt', mode='w', encoding='utf8') as output_file:
        get_text(text, output_file)
    all_lines = []
    with open('/cgi-bin/web_text.txt', mode='r', encoding='utf8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            all_lines.append(lines[i])
    get_topic_number(all_lines, lda)
    #get_topic_number(text, lda)

    if 'click' in str(text):
        with open('/create-chunk/history/log/click_log.txt', mode='a') as f:
            f.write(str(datetime.datetime.now())[:-7] + ' ' + str(text) + '\n')
            exit()
    with open('/cgi-bin/topic.txt',mode='r') as looking_file:
        make_looking(looking_file)
    
