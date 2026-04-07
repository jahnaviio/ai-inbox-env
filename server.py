<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: Arial; text-align:center; margin-top:50px;">

            <h1>AI Email Assistant</h1>

            <button onclick="runAgent()">Run AI</button>

            <pre id="output" style="
                margin-top:20px;
                text-align:left;
                width:60%;
                margin-left:auto;
                margin-right:auto;
                white-space:pre-wrap;
                word-wrap:break-word;
                border:1px solid #ccc;
                padding:15px;
            "></pre>

            <script>
                async function runAgent() {
                    document.getElementById("output").innerText = "Running...";

                    const res = await fetch("/run");
                    const data = await res.text();

                    document.getElementById("output").innerText = data;
                }
            </script>

        </body>
    </html>
    """


@app.get("/run")
def run():
=======
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: Arial; text-align:center; margin-top:50px;">

            <h1>AI Email Assistant</h1>

            <button onclick="runAgent()">Run AI</button>

            <pre id="output" style="
                margin-top:20px;
                text-align:left;
                width:60%;
                margin-left:auto;
                margin-right:auto;
                white-space:pre-wrap;
                word-wrap:break-word;
                border:1px solid #ccc;
                padding:15px;
            "></pre>

            <script>
                async function runAgent() {
                    document.getElementById("output").innerText = "Running...";

                    const res = await fetch("/run");
                    const data = await res.text();

                    document.getElementById("output").innerText = data;
                }
            </script>

        </body>
    </html>
    """


@app.get("/run")
def run():
>>>>>>> cba4c8e (removed pycache folders)
    return subprocess.getoutput("py gmail_ai_agent.py")