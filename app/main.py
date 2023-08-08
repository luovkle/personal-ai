import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)


@app.route("/")
def read_profile():
    profile = {
        "name": os.getenv("PROFILE_NAME", ""),
    }
    return render_template("profile.html", profile=profile)
