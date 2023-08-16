import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)


@app.route("/")
@app.route("/profile")
def profile():
    profile = {
        "name": os.getenv("PROFILE_NAME", ""),
    }
    return render_template("profile.html", profile=profile)


@app.route("/chat")
def chat():
    profile = {
        "name": os.getenv("PROFILE_NAME", ""),
        "picture": {
            "url": "",
        },
    }
    return render_template("chat.html", profile=profile)


@app.route("/settings")
def settings():
    return render_template("settings.html")
