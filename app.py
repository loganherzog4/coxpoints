from dotenv import load_dotenv
from flask import Flask, request
from src.data.data import DataService

import os

app = Flask(__name__)
data_service = DataService()

load_dotenv()


@app.route("/")
def root():
    return "CoX Points calculator."


@app.route("/generate-csv", methods=["GET"])
def generate_csv():
    base_path = request.args.get("basePath")
    if base_path is None or base_path == '':
        base_path = os.environ["BASE_PATH"]
    try:
        folders = request.args.get("folders").split(',')
    except AttributeError:
        folders = os.environ["FOLDERS"].split(',')

    data_service.generate_csv(base_path=base_path, folders=folders)

    return "Called generate-csv."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
