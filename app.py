# Version 3.0

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import random
import os
from datetime import timedelta


app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "the_improv_cooperative"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)

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
category = None

def newSuggestion(list):
    return random.choice(list)

@app.route("/")
def index():

    first_click = session.get("first_click", False)
    print(f"Index route: first_click = {first_click}")  # Debugging
    if first_click:
        # Redirect to the one-word page if the first click has already occurred
        return redirect(url_for("oneword"))
    familyFriendly = session.get("familyFriendly", False)
    return render_template("index.html", familyFriendly=familyFriendly)

@app.route("/clear-session")
def clear_session():
    session.clear()
    # Reinitialize session variables with default values
    session["first_click"] = False
    session["familyFriendly"] = False
    session["category"] = "nouns"
    print("Session cleared and reinitialized with default values.")
    return "Session cleared and reinitialized!"

@app.route("/firstnew", methods=["POST"])
def firstnew():
    return redirect(url_for("oneword"))  # Redirect to /one-word on the first click
        
@app.route("/new", methods=["POST"])
def new():
   
    # Check if a category is set in the session
    category = session.get("category", "nouns")

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
    else:
        return "Invalid category", 400
    
    familyFriendly = session.get("familyFriendly", False)
    if familyFriendly:
        filtered_list = suggestions
    else:
        filtered_list = suggestions + flagged

    suggestion = newSuggestion(filtered_list)
    return suggestion, 200, {"Content-Type": "text/plain"}

@app.route("/toggle-family-friendly", methods=["POST"])
def toggle_family_friendly():
    data = request.get_json()
    session['familyFriendly'] = data.get("familyFriendly", False)
    print(f"Family-friendly filter set to: {session['familyFriendly']}") 
    return jsonify(success=True)


@app.route("/oneword")
def oneword():
    global list 
    session['category'] = "nouns"
    familyFriendly = session.get("familyFriendly", False)
    print(f"Family-friendly filter retrieved: {familyFriendly}")  # Debugging
    suggestions, flagged = nounsFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("oneword.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

@app.route("/location")
def location():
    global list
    session['category'] = "locations"
    familyFriendly = session.get("familyFriendly")
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
    familyFriendly = session.get("familyFriendly")
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
    familyFriendly = session.get("familyFriendly")
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
    familyFriendly = session.get("familyFriendly")
    suggestions, flagged = genresFile()
    if familyFriendly:
        list = suggestions
    else:
        list = suggestions + flagged
    suggestion = newSuggestion(list)
    return render_template("genre.html", suggestion=suggestion, list=list, familyFriendly=familyFriendly)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


'''
FAMILY FRIENDLY filter is NOT working correctly. 
'''