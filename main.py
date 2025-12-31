from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, tempfile, os, json

app = FastAPI()

class RunRequest(BaseModel):
    entry: str
    files: dict
    timeout: int = 5

@app.post("/run")
def run(req: RunRequest):
    with tempfile.TemporaryDirectory() as tmp:
        for name, content in req.files.items():
            path = os.path.join(tmp, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)

        try:
            result = subprocess.run(
                ["python3", req.entry],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=req.timeout
            )

            return (
                result.stdout +
                ("\n" + result.stderr if result.stderr else "")
            )

        except subprocess.TimeoutExpired:
            return "Error: Execution timed out"
