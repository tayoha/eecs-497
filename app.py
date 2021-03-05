import requests
from flask import Flask, jsonify, request, render_template, send_from_directory, url_for, redirect
app = Flask(__name__)

API_KEY = '20169026-d45bc99749bd521df7aa7b5f4'
CONTEXT = {"photos": {}}
# TODO: clear context when done with query
@app.route('/', methods=["GET", "POST"])
def print_form():
    global CONTEXT
    if request.method == "GET":
        # serve HTML page
        print("Received GET request")
        return render_template("index.html")
    else:
        # handle text from submitted form
        print(request.json) # prints form input
        text_book = request.json["text_book"]
        text_book_words = text_book.split()
        for word in text_book_words:
            # make call to image API
            url = "https://pixabay.com/api/?key="+API_KEY+"&q="+word
            response = requests.get(url)
            #print(response.json())
            if response.status_code == 200:
                print("Success!")
            # add word, link pair to dictionary for new HTML rendering
            # TODO: check that response has hits
            img_link = response.json()["hits"][0]["webformatURL"]
            print("img_link: " + img_link)
            CONTEXT["photos"][word] = img_link
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