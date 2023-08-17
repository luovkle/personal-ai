import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

data = {
    "profile": {
        "name": os.getenv("PROFILE_NAME", ""),
        "picture": os.getenv("PROFILE_PICTURE", ""),
    }
}

app = Flask(__name__)


@app.route("/")
@app.route("/profile")
def profile():
    return render_template("profile.html", profile=data["profile"])


@app.route("/chat")
def chat():
    return render_template("chat.html", profile=data["profile"])


@app.route("/settings")
def settings():
    return render_template("settings.html")
