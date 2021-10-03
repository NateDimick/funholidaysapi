from flask import Flask, render_template, request
from flask_cors import CORS
import markdown

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/docs")
def docs():
    with open("README.md", 'r', encoding="UTF-8") as f:
        file = f.read()
        readme = markdown.markdown(file, extensions=["fenced_code"])
    return render_template("docs.html", md=readme)


@app.route("/demo")
def lookup():
    args = request.args        
    if args.get("kw", ""):
        return render_template("lookup.html", keyword=args["kw"])
    elif args.get("dt", ""):
        return render_template("lookup.html", date=args["dt"])
    else:
        return render_template("lookup.html")
        