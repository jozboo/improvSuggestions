from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import os


app = Flask(__name__, static_folder="static", template_folder="templates")

list = []

def newSuggestion(list):
    return random.choice(list)

@app.route("/")
def index():
    global list 
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "nouns.json")

    with open(suggestions_file_path) as nouns:
        data = json.load(nouns)
        list = data.get("nouns", [])
    suggestion = newSuggestion(list)
    return render_template("index.html", suggestion=suggestion, list=list)

@app.route("/new", methods=["POST"])
def new():
    suggestion = newSuggestion(list)
    return suggestion, 200, {"Content-Type": "text/plain"}

@app.route("/location")
def location():
    global list
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "locations.json")

    with open(suggestions_file_path) as locations:
        data = json.load(locations)
        list = data.get("locations", [])
    suggestion = newSuggestion(list)
    return render_template("location.html", suggestion=suggestion, list=list)

@app.route("/relationship")
def relationship():
    global list
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "relationships.json")
    with open(suggestions_file_path) as relationships:
        data = json.load(relationships)
        list = data.get("relationships", [])
    suggestion = newSuggestion(list)
    return render_template("relationship.html", suggestion=suggestion, list=list)

@app.route("/occupation")
def occupation():
    global list
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "occupations.json")
    with open(suggestions_file_path) as occupations:
        data = json.load(occupations)
        list = data.get("occupations", [])
    suggestion = newSuggestion(list)
    return render_template("occupation.html", suggestion=suggestion, list=list)

@app.route("/genre")
def genre():
    global list
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "genres.json")
    with open(suggestions_file_path) as genres:
        data = json.load(genres)
        list = data.get("genres", [])
    suggestion = newSuggestion(list)
    return render_template("genre.html", suggestion=suggestion, list=list)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)