import os
import json

from dotenv import load_dotenv

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
