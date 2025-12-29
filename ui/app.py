from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "outputs" / "latest.json"


@app.get("/", response_class=HTMLResponse)
def index():
    html_path = Path(__file__).parent / "templates" / "index.html"
    return html_path.read_text()


@app.get("/data")
def get_data():
    if not OUTPUT_FILE.exists():
        return {"error": "No Cascada output found"}
    return json.loads(OUTPUT_FILE.read_text())
