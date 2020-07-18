from django.conf import settings

TEMPLATES_DIR = settings.REPO_DIR / "templates"
USER_SESSIONS = settings.REPO_DIR / "sessions.json"
PROJECTS = settings.REPO_DIR / "projects.json"

BINARY_EXTENSIONS = {
    ".gif",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".zip",
}
