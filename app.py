import requests
from flask import Flask, jsonify, request, render_template, send_from_directory, url_for, redirect
app = Flask(__name__)

API_KEY = '20169026-d45bc99749bd521df7aa7b5f4'
CONTEXT = {"photos": {}}

"""test input:
hello there. pictures are a good way to do stuff. baseball is cool. dogs are cute. cats are found in the park at night. soccer is a sport for nerds. potato is my nickname. michigan is where i go to school. school sucks. coding is fun sometimes. stupid is this. yoda talks like this. star wars is a series that i'm watching. basketball is also cool. sports are fun in general. poker is a fun game where people cry. crying is sad. money is nice. trees are green. fans only. shit is what i'm saying dawg. amigo.
"""

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
        section_size = num_sentences // slider_val # has to be an integer
        text_book_sections = []
        for idx in range(0, num_sentences, section_size):
            if idx + section_size < num_sentences:
                text_book_sections.append(". ".join(text_book_sentences[idx:(idx + section_size)]))
            else:
                text_book_sections.append(". ".join(text_book_sentences[idx:]))
        # use first word of each section to search
        text_book_words = []
        for section in text_book_sections:
            word = section.split()[0]
            text_book_words.append(word)
        # perform image api search
        for idx, word in enumerate(text_book_words):
            # make call to image API
            url = "https://pixabay.com/api/?key="+API_KEY+"&q="+word
            response = requests.get(url)
            # print(response.json())
            if response.status_code == 200:
                print("Success!")
            # add word, link pair to dictionary for new HTML rendering
            if response.json()["hits"]:
                img_link = response.json()["hits"][0]["webformatURL"]
                print("img_link: " + img_link)
                CONTEXT["photos"][text_book_sections[idx]] = img_link
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