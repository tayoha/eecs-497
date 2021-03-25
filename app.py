import requests
import json
from flask import Flask, jsonify, request, render_template, send_from_directory, url_for, redirect
from serpapi import GoogleSearch

"""
params = {
  "q": "Apple",
  "tbm": "isch",
  "ijn": "0",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()
images_results = results['images_results']
"""
app = Flask(__name__)

API_KEY = '20169026-d45bc99749bd521df7aa7b5f4'
CONTEXT = {"photos": {}}


@app.route('/', methods=["GET", "POST"])
def print_form():
    global CONTEXT
    if request.method == "GET":
        # serve HTML page
        return render_template("index.html")
    else:
        # handle text from submitted form
        CONTEXT["photos"].clear()
        text_book = request.json["text_book"]
        slider_val = int(request.json["slider_val"])
        # split text into sections
        text_book_sentences = text_book.split('.')
        text_book_sentences = text_book_sentences[:-1] # get rid of last empty string (after last sentence)
        num_sentences = len(text_book_sentences)
        text_book_sections = []
        for idx in range(0, num_sentences, slider_val):
            if idx + slider_val < num_sentences:
                text_book_sections.append(". ".join(text_book_sentences[idx:(idx + slider_val)]))
            else:
                text_book_sections.append(". ".join(text_book_sentences[idx:]))
        # summarize each sentence
        url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer"
        summaries = []
        for section in text_book_sections:
            payload = {
                "url": "",
                "text": section,
                "sentnum": 1
            }
            headers = {
                'content-type': "application/json",
                'x-rapidapi-key': "3370a90c6bmsh4469eda97977206p1dbffdjsne99d3fc5a7b0",
                'x-rapidapi-host': "textanalysis-text-summarization.p.rapidapi.com"
            }
            summary = json.loads(requests.request("POST", url, data=json.dumps(payload), headers=headers).text)
            summaries.append(summary["sentences"][0])
            print(summary["sentences"])
        # perform image api search
        for idx, summary in enumerate(summaries):
            # make call to image API
            #url = "https://pixabay.com/api/?key="+API_KEY+"&q="+summary
            params = {
                "q": summary,
                "tbm": "isch",
                "ijn": "0",
                "api_key": "secret_api_key"
            }
            search = GoogleSearch(params)
            results = search.get_dict()
            images_results = results['images_results']
            print(images_results)
            # TODO: inspect response and create CONTEXT
            """response = requests.get(url)
            # print(response.json())
            if response.status_code == 200:
                print("Success!")
            # add summary, link pair to dictionary for new HTML rendering
            if response.json()["hits"]:
                img_link = response.json()["hits"][0]["webformatURL"]
                print("img_link: " + img_link)
                CONTEXT["photos"][summaries[idx]] = img_link"""
        return redirect(url_for('view_results'))

@app.route('/view_results', methods=["GET"])
def view_results():
    global CONTEXT
    return render_template("imgs.html", **CONTEXT)

# handle GET requests for javascript files
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == "__main__":
    app.run(port=3001)