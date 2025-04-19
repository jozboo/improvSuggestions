# Version 2.0

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import random
import os


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "your_secret_key"  # Replace with a strong secret key

def nounsFile():
    nouns_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "nouns.json")

    with open(nouns_file_path) as nouns:
        data = json.load(nouns)
        suggestions = data.get("nouns", [])
        flagged = data.get("flagged", [])

    return suggestions, flagged

def locationsFile():
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "locations.json")

    with open(suggestions_file_path) as locations:
        data = json.load(locations)
        suggestions = data.get("locations", [])
        flagged = data.get("flagged", [])

    return suggestions, flagged

def relationshipsFile():
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "relationships.json")

    with open(suggestions_file_path) as relationships:
        data = json.load(relationships)
        suggestions = data.get("relationships", [])
        flagged = data.get("flagged", [])

    return suggestions, flagged

def occupationsFile():
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "occupations.json")

    with open(suggestions_file_path) as occupations:
        data = json.load(occupations)
        suggestions = data.get("occupations", [])
        flagged = data.get("flagged", [])

    return suggestions, flagged

def genresFile():
    suggestions_file_path = os.path.join(os.path.dirname(__file__), "suggestions", "genres.json")

    with open(suggestions_file_path) as genres:
        data = json.load(genres)
        suggestions = data.get("genres", [])
        flagged = data.get("flagged", [])

    return suggestions, flagged

list = []
category = "nouns"

def newSuggestion(list):
    return random.choice(list)

@app.route("/")
def index():
    global list 
    session['category'] = "nouns"
    familyFriendly = session.get("familyFriendly", False)
    suggestions, flagged = nounsFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("index.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

@app.route("/new", methods=["POST"])
def new():
    # Get the category from the session
    category = session.get("category", "nouns")  # Default to "nouns" if no category is set

    if category == "nouns":
        suggestions, flagged = nounsFile()
    elif category == "locations":
        suggestions, flagged = locationsFile()
    elif category == "relationships":
        suggestions, flagged = relationshipsFile()
    elif category == "occupations":
        suggestions, flagged = occupationsFile()
    elif category == "genres":
        suggestions, flagged = genresFile()
    
    familyFriendly = session.get("familyFriendly", False)
    if familyFriendly:
        filtered_list = suggestions  # Exclude flagged items
    else:
        filtered_list = suggestions + flagged  # Include flagged items

    suggestion = newSuggestion(filtered_list)
    return suggestion, 200, {"Content-Type": "text/plain"}

@app.route("/toggle-family-friendly", methods=["POST"])
def toggle_family_friendly():
    data = request.get_json()
    session['familyFriendly'] = data.get("familyFriendly", False)
    return jsonify(success=True)

@app.route("/location")
def location():
    global list
    session['category'] = "locations"
    familyFriendly = session.get("familyFriendly", False)
    suggestions, flagged = locationsFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("location.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

@app.route("/relationship")
def relationship():
    global list
    session['category'] = "relationships"
    familyFriendly = session.get("familyFriendly", False)
    suggestions, flagged = relationshipsFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("relationship.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

@app.route("/occupation")
def occupation():
    global list
    session['category'] = "occupations"
    familyFriendly = session.get("familyFriendly", False)
    suggestions, flagged = occupationsFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("occupation.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

@app.route("/genre")
def genre():
    global list
    session['category'] = "genres"
    familyFriendly = session.get("familyFriendly", False)
    suggestions, flagged = genresFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("genre.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)