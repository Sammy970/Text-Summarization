from ast import Str
import requests
from flask import Flask, redirect, render_template, url_for
from flask import request as req

app = Flask(__name__)
@app.route("/", methods = ["GET","POST"])

def Index():
    return render_template("index.html")

# @app.route("/Summarize",methods={"GET","POST"})

@app.route("/Summarize/", methods={"GET","POST"})
def Summarize():
    if req.method=="POST":

            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": "Bearer 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"}
            
            data= req.form["data"]
            

            # minL= 100	
            # maxL= int(req.form["maxL"])

            minL= int(req.form["minL"])
            maxL = 2000

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            output = query({
                "inputs":data,
                # "parameters": {"min_length`":minL,"max_length":maxL},
                "parameters": {"min_length":minL,"max_length":1000},

            })[0]

            return render_template("index.html",result=output["summary_text"])
    else:
        return render_template("index.html")

@app.route('/textRank/', methods={"GET","POST"})
def textRank():
    if req.method=="POST":
        
            text = req.form["data"]

            from tracemalloc import stop
            import spacy
            from spacy.lang.en.stop_words import STOP_WORDS
            from string import punctuation

            stopwords = list(STOP_WORDS)

            nlp = spacy.load('en_core_web_sm')

            doc = nlp(text)

            tokens = [token.text for token in doc]
            # print(tokens)

            punctuation = punctuation + '\n'
            # print(punctuation)

            word_frequencies = {}
            for word in doc:
                if word.text.lower() not in stopwords:
                    if word.text.lower() not in punctuation:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1

            # print(word_frequencies)

            max_frequency = max(word_frequencies.values())

            # print(max_frequency)

            for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word]/max_frequency

            # print(word_frequencies)

            sentence_tokens = [sent for sent in doc.sents]
            # print(sentence_tokens)


            sentence_scores = {}
            for sent in sentence_tokens:
                for word in sent:
                    if word.text.lower() in word_frequencies.keys():
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]
            # print(sentence_scores)

            from heapq import nlargest

            select_length = int(len(sentence_tokens)*0.3)
            # print(select_length)

            summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
            # print(summary)

            final_summary = [word.text for word in summary]

            summary = ' '.join(final_summary)
            # print(summary)

            # print(len(text))
            # print(len(summary))

            return render_template("textRank.html",TextRankresult=summary)
    else:
        return render_template("textRank.html")

if __name__ == "__main__":
    app.run(debug=True)
