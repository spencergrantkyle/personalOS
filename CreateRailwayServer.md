Here’s a full starter kit for your Railway server — code, instructions, and a clean prompt for a coding agent that will generate and deploy your repo. This sets you up with a Python API that can receive CSVs, process them with your logic, and save results.

⸻

1. Repository Structure

csv-runner/
├── main.py               # FastAPI app (API entrypoint)
├── requirements.txt
├── scripts/
│   └── process_csv.py    # Your processing logic goes here
├── Dockerfile
└── Procfile


⸻

2. Files & Code

requirements.txt

fastapi
uvicorn
pandas
python-multipart

main.py

from fastapi import FastAPI, UploadFile, Form
import pandas as pd
import os
from scripts.process_csv import process_dataframe

app = FastAPI()
DATA_PATH = "/data"

@app.get("/")
def root():
    return {"status": "ready", "files": os.listdir(DATA_PATH)}

@app.post("/process")
async def process(file: UploadFile, prompt: str = Form(...)):
    # Save uploaded CSV
    input_path = os.path.join(DATA_PATH, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Load CSV and process
    df = pd.read_csv(input_path)
    df = process_dataframe(df, prompt)

    # Write output
    output_path = input_path.replace(".csv", "_out.csv")
    df.to_csv(output_path, index=False)
    return {"message": "processed", "output_file": output_path}

scripts/process_csv.py

import pandas as pd

def process_dataframe(df: pd.DataFrame, prompt: str) -> pd.DataFrame:
    """
    Apply your logic to every row of the DataFrame.
    Replace this with your existing formula update logic.
    """
    df["updated_formula"] = df.apply(lambda row: f"Processed({row.to_dict()}, prompt='{prompt}')", axis=1)
    return df

Dockerfile

FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8000

# Launch with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Procfile (optional, but makes Railway detect your process)

web: uvicorn main:app --host 0.0.0.0 --port $PORT


⸻

3. Deployment Instructions
	1.	Create a GitHub repo with the above files.
	2.	Push the code to main.
	3.	Go to Railway Dashboard → New Project → Deploy from GitHub, pick the repo.
	4.	In the service settings:
	•	Add a volume mounted at /data.
	•	Railway will automatically detect your Python service and deploy.
	5.	Open the public URL and hit / — you should see {"status": "ready"}.

⸻

4. How to Use
	•	Upload a CSV and prompt via cURL or Postman:

curl -X POST "https://<your-railway-url>/process" \
  -F "file=@input.csv" \
  -F "prompt=Rewrite formulas with new named range"

	•	Output CSV will be stored in /data with _out.csv suffix.

⸻

5. Prompt for a Coding Agent

Here’s a copy-paste ready instruction for Cursor/Replit/Claude/Code Interpreter:

Goal: Build a GitHub repository called csv-runner for deploying on Railway.

Requirements:
	•	Use Python 3.11 + FastAPI.
	•	Include a main.py exposing:
	•	GET / endpoint that lists files in /data.
	•	POST /process endpoint that:
	•	Accepts a CSV file + text prompt.
	•	Saves file to /data.
	•	Loads it into pandas, applies a function process_dataframe(df, prompt), writes output CSV back to /data.
	•	Put process_dataframe inside scripts/process_csv.py.
	•	Add requirements.txt with fastapi, uvicorn, pandas, python-multipart.
	•	Include a Dockerfile to run uvicorn main:app --host 0.0.0.0 --port 8000.
	•	Add a Procfile with web: uvicorn main:app --host 0.0.0.0 --port $PORT.
	•	Organize code cleanly, follow Python best practices.
	•	Output the final repo structure and full file contents.

⸻

