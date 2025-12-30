from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False
    ) as f:
        f.write(code)
        filename = f.name

    try:
        result = subprocess.run(
            ["python3", filename],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
    except Exception as e:
        output = str(e)

    os.remove(filename)
    return jsonify({"output": output})


@app.route("/")
def home():
    return "Pythoniser server is running"
