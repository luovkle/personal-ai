import os
import json
from secrets import token_urlsafe
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, render_template, session
from flask_socketio import join_room, leave_room, send, SocketIO

from app.utils.chatgpt import get_completion
from app.utils.repository import get_repo_data

load_dotenv()

data = {
    "profile": {
        "name": os.getenv("PROFILE_NAME", ""),
        "picture": os.getenv("PROFILE_PICTURE", ""),
        "role": os.getenv("PROFILE_ROLE", ""),
        "about": os.getenv("PROFILE_ABOUT", ""),
    },
    "contact": {
        "github": os.getenv("PROFILE_CONTACT_GITHUB", ""),
        "linkedin": os.getenv("PROFILE_CONTACT_LINKEDIN", ""),
    },
    "resume": os.getenv("RESUME", ""),
    "projects": json.loads(os.getenv("PROJECTS", "[]")),
}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY", token_urlsafe(64))
socketio = SocketIO(app)


@app.route("/")
@app.route("/profile")
def profile():
    projects = [get_repo_data(repo) for repo in data["projects"]]
    return render_template(
        "profile.html",
        profile=data["profile"],
        contact=data["contact"],
        resume=data["resume"],
        projects=projects,
    )


@app.route("/chat")
def chat():
    if "id" not in session:
        session["id"] = str(uuid4())
    return render_template("chat.html", profile=data["profile"])


@app.route("/settings")
def settings():
    return render_template("settings.html")


@socketio.on("connect")
def on_connect():
    id = session.get("id")
    if id:
        join_room(id)


@socketio.on("message")
def on_message(request):
    id = session.get("id")
    if id:
        response = {"data": request["data"]}
        send(response, to=id)
        response = {
            "data": get_completion(request["data"]),
            "owner": "bot",
            "botData": data["profile"],
        }
        send(response, to=id)


@socketio.on("disconnect")
def on_disconnect():
    if "id" in session:
        leave_room(id)
