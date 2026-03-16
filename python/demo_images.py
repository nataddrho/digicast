from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

SHM_FOLDER = "shm"

# Ensure folder exists
os.makedirs(SHM_FOLDER, exist_ok=True)

# Serve files from shm folder
@app.route("/shm/<path:filename>")
def serve_file(filename):
    file_path = os.path.join(SHM_FOLDER, filename)

    # Prevent directory traversal
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(SHM_FOLDER, filename)

# Index page listing all files
@app.route("/")
@app.route("/index.htm")
def index():
    files = [
        f for f in os.listdir(SHM_FOLDER)
        if os.path.isfile(os.path.join(SHM_FOLDER, f))
    ]

    html = """
    <html>
    <head>
        <title>SHM File List</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>Files in /shm</h1>
        <ul>
    """

    for f in files:
        html += f'<li><a href="/shm/{f}">{f}</a></li>'

    html += """
        </ul>
        <p>Page auto-refreshes every 5 seconds.</p>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)