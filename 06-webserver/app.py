import os
import requests
from flask import Flask, render_template


app = Flask(__name__)

ARGOCD_SERVER = os.getenv("ARGOCD_SERVER") # o svc interno de kubernetes ;) 
ARGOCD_TOKEN = os.getenv("ARGOCD_TOKEN")


def get_apps():
    headers = {"Authorization": f"Bearer {ARGOCD_TOKEN}"}
    url = f"{ARGOCD_SERVER}/api/v1/applications"
    resp = requests.get(url, headers=headers, verify=False)
    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])


@app.route("/")
def index():
    apps = get_apps()
    return render_template("index.html", apps=apps, argocd_server=ARGOCD_SERVER)

@app.route("/detailed")
def detailed():
    apps = get_apps()
    return render_template("detailed.html", apps=apps, argocd_server=ARGOCD_SERVER)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
